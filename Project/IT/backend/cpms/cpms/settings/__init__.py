import warnings
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env(DEBUG=(bool, False))  # set default values and casting

# Disable warnings if the .env file is not found
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    environ.Env.read_env(BASE_DIR / 'environments' / '.env')

MODE = env('MODE')

if MODE == 'development':
    from .development import *
elif MODE == 'production':
    from .production import *
