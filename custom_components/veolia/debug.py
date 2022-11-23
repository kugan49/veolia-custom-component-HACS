import logging

_LOGGER = logging.getLogger(__name__)


def decoratorexceptionDebug(f):
    def decoratorfunction(*args, **kwargs):
        result = None
        try:
            _LOGGER.debug(f"Start function {f.__name__}")
            result = f(*args, **kwargs)
            _LOGGER.debug(f"End function {f.__name__}")
        except Exception as e:
            _LOGGER.error(f"Error in function {f.__name__}: {e}")
        return result

    return decoratorfunction
