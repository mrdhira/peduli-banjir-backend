from .base import *
from .base import env
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)
