import sys
sys.path.append('.')

from daily_informer.logger import get_logger

logger = get_logger("TelegramApiError")


class TelegramError(Exception):
    def __init__(self, message=None, error=Exception):
        logger.error(f'Exception has been caught: {error} message: {message}')

class InvalidApiToken(TelegramError):
    def __init__(self, message):
        super().__init__(message=message, error=InvalidApiToken)

class NoConnectionError(TelegramError):
    def __init__(self, message, error):
        super().__init__(message=message, error=NoConnectionError)



