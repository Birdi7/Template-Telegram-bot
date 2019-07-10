from .logger_middleware import LoggingMiddleware
from .updater import UpdateUserMiddleware


def on_startup(dp):
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(UpdateUserMiddleware())
