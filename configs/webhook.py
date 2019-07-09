# Here is your webhook config data such as host, port etc.
import os

WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PORT = os.getenv('WEBHOOK_PORT')
WEBHOOK_LISTEN = os.getenv('WEBHOOK_LISTEN')
WEBHOOK_SSL_CERT_PATH = os.getenv('WEBHOOK_SSL_CERT_PATH')
WEBHOOK_SSL_PRIV_PATH = os.getenv('WEBHOOK_SSL_PRIV_PATH')
