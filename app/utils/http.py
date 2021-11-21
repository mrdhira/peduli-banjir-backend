import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def format_exception_string(error):
    """Format exception string with name of error and a brief description."""
    return "{0}: {1}".format(type(error).__name__, error.args)


def generic_get(
    request,
    model_method,
    response_serializer,
    request_serializer=None,
    success_message=None,
    serializer_error_message=None,
    not_found_error_message=None,
    failure_message=None,
    many=False,
    context=None,
    content_type=None,
    protected=False,
):
    """Used for generic GET controller actions.

    Required args:
        request: Request object
        model_method: Model method to call
        response_serializer: Serializer for response
    Optional args:
        request_serializer: If provided, will attempt to
        serialize the GET request's query params and pass
        the result to `get_method`
        many: If True, will pass it as many=True to response_serializer
        which attempts to serialize it as a list of objects
        context: A optional dict of context variables
        such as `user_id` and/or `offer_id`
        content_type: Specifies a successful Response's `content_type`,
        defaults to application/json (see DEFAULT_RENDERER_CLASSES).

        success_message: Flash message to display upon 200
        serializer_error_message: Flash message to display upon 400
        not_found_error_message: Flash message to display upon 404
        failure_message: Flash message to display upon 500
    """

    serializer = None

    if request_serializer:
        serializer = request_serializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": serializer_error_message or "Some fields are invalid",
                    "error": serializer.errors,
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    try:
        kwargs = context or {}
        if serializer:
            kwargs["fields"] = serializer.data.copy()
        if protected:
            kwargs["fields"]["user"] = request.user
        result = model_method(**kwargs)

    except ObjectDoesNotExist as error:
        default_not_found_error_message = (
            "Collection not found" if many else "Detail not found"
        )

        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "message": not_found_error_message or default_not_found_error_message,
                "error": format_exception_string(error),
                "data": {},
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as error:
        return Response(
            {
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": failure_message or "Server error",
                "error": format_exception_string(error),
                "data": {},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    default_success_message = "Object retrieved" if many else "Collection retrieved"
    result_payload = response_serializer(
        result,
        many=many,
        context={"request": request},
    ).data

    return Response(
        {
            "status": status.HTTP_200_OK,
            "message": success_message or default_success_message,
            "error": None,
            "data": result_payload,
        },
        status=status.HTTP_200_OK,
        content_type=content_type,
    )


def generic_post(
    request,
    request_serializer,
    response_serializer,
    create_method,
    empty_body=False,
    success_message=None,
    serializer_error_message=None,
    not_found_error_message=None,
    database_error_message=None,
    context=None,
    protected=False,
):
    """Used for generic POST controller actions."""

    if not empty_body:
        if not request_serializer:
            raise ValueError(
                "empty_body was set to False, but a request serializer was not specified."
            )  # NOQA

        serializer = request_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(serializer.errors)
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": serializer_error_message or "Some fields are invalid",
                    "error": serializer.errors,
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    try:
        kwargs = context or {}
        if not empty_body and serializer:
            kwargs["fields"] = serializer.data.copy()
        if protected:
            kwargs["fields"]["user"] = request.user
        if request.FILES:
            kwargs["fields"]["files"] = request.FILES
        created_instance = create_method(**kwargs)

    except ObjectDoesNotExist as error:
        default_not_found_error_message = "Detail not found"
        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "message": not_found_error_message or default_not_found_error_message,
                "error": format_exception_string(error),
                "data": {},
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as error:
        return Response(
            {
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": database_error_message
                or "An error occurred while saving to the database",
                "error": format_exception_string(error),
                "data": {},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    result_payload = response_serializer(
        created_instance,
        context={"request": request},
    ).data

    return Response(
        {
            "status": status.HTTP_200_OK,
            "message": success_message or "Successfully created",
            "error": None,
            "data": result_payload,
        },
        status=status.HTTP_200_OK,
    )


def generic_put(
    request,
    object_id,
    response_serializer,
    update_method,
    request_serializer=None,  # NOQA
    empty_body=False,
    success_message=None,
    serializer_error_message=None,
    not_found_error_message=None,
    database_error_message=None,
    context=None,
    protected=False,
):
    """
    Used for generic detail PUT controller actions.

    Only querying by ID is supported. This is by design as this is meant to be
    a generic function. If querying by other parameters is required, please
    use a different function.
    """

    if not empty_body:
        if not request_serializer:
            raise ValueError(
                "empty_body was set to False, but a request serializer was not specified."
            )  # NOQA

        serializer = request_serializer(data=request.data, context=context)
        if not serializer.is_valid():
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": serializer_error_message or "Some fields are invalid",
                    "error": serializer.errors,
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    try:
        kwargs = context or {}
        if not empty_body and serializer:
            kwargs["fields"] = serializer.data.copy()
            kwargs["fields"]["object_id"] = object_id
        if protected:
            kwargs["fields"]["user"] = request.user
        updated_instance = update_method(**kwargs)

    except ObjectDoesNotExist as error:
        default_not_found_error_message = (
            "Collection not found" if many else "Detail not found"
        )

        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "message": not_found_error_message or default_not_found_error_message,
                "error": format_exception_string(error),
                "data": {},
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as error:
        return Response(
            {
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": database_error_message
                or "An error occurred while saving to the database",
                "error": format_exception_string(error),
                "data": {},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERRORs,
        )

    result_payload = response_serializer(
        updated_instance,
        context={"request": request},
    ).data

    return Response(
        {
            "status": status.HTTP_200_OK,
            "message": success_message or "Successfully updated",
            "error": None,
            "data": result_payload,
        },
        status=status.HTTP_200_OK,
    )


def generic_delete(
    request,
    object_id,
    delete_method,
    not_found_error_message=None,
    failure_message=None,
    protected=False,
):
    """
    Used for generic detail DELETE controller actions.

    Only querying by ID is supported. This is by design as this is meant to be
    a generic function. If querying by other parameters is required, please
    use a different function.
    """

    try:
        kwargs = {}
        kwargs["fields"] = {}
        kwargs["fields"]["object_id"] = object_id
        if protected:
            kwargs["fields"]["user"] = request.user
        deleted_instance = delete_method(**kwargs)
    except ObjectDoesNotExist as error:
        default_not_found_error_message = (
            "Collection not found" if many else "Detail not found"
        )

        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "message": not_found_error_message or default_not_found_error_message,
                "error": format_exception_string(error),
                "data": {},
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as error:
        return Response(
            {
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": failure_message or "There was an error",
                "error": format_exception_string(error),
                "data": {},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(
        {
            "status": status.HTTP_200_OK,
            "message": "Ok",
            "error": None,
            "data": None,
        },
        status=status.HTTP_200_OK,
    )
