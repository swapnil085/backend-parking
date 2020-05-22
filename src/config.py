# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@db/parking'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads
# A common general assumption is using 2 per available cores
# to handle incoming requests using one
# perform backgorund operations using the other
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure and unique secret key for signing the data
CSRF_SESSION_KEY = 'secret'

# Secret key for signing cookies
SECRET_KEY = 'secret'

MAIL_SERVER='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'sbuchke085@gmail.com'
MAIL_PASSWORD = ''
MAIL_USE_TLS = False
MAIL_USE_SSL = True
