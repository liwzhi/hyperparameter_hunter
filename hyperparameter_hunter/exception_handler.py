"""This module defines a few custom Exception classes, and it provides the means for Exceptions to be added to the Heartbeat
result files of Experiments

Related
-------
:mod:`hyperparameter_hunter.reporting`
    This module executes :func:`hyperparameter_hunter.exception_handler.hook_exception_handler` to ensure that any raised
    Exceptions are also recorded in the Heartbeat files of the Experiment for which the Exception was raised in order to assist
    in debugging"""
##################################################
# Import Miscellaneous Assets
##################################################
import logging
import sys

logger = logging.getLogger(__name__)

# noinspection PyProtectedMember
stream_handler = logging._StderrHandler()
# stream_handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(stream_handler)


def handle_exception(exception_type, exception_value, exception_traceback):
    """Intercept raised exceptions to ensure they are included in an Experiment's log files

    Parameters
    ----------
    exception_type: Exception
        The class type of the exception that was raised
    exception_value: Str
        The message produced by the exception
    exception_traceback: Exception.traceback
        The traceback provided by the raised exception

    Raises
    ------
    SystemExit
        If `exception_type` is a subclass of KeyboardInterrupt"""
    if issubclass(exception_type, KeyboardInterrupt):
        logging.error('KEYBOARD INTERRUPT!')
        sys.__excepthook__(exception_type, exception_value, exception_traceback)
        raise SystemExit

    logging.critical(
        'Uncaught exception!   {}: {}'.format(exception_type.__name__, exception_value),
        exc_info=(exception_type, exception_value, exception_traceback)
    )


def hook_exception_handler():
    """Set `sys.excepthook` to :func:`hyperparameter_hunter.exception_handler.handle_exception`"""
    sys.excepthook = handle_exception


class EnvironmentInactiveError(Exception):
    def __init__(self, message=None, extra=''):
        """Exception raised when an active instance of :class:`hyperparameter_hunter.environments.Environment` is not detected

        Parameters
        ----------
        message: String, or None, default=None
            A message to provide upon raising `EnvironmentExceptionError`
        extra: String, default=''
            Extra content to append onto the end of `message` before raising the Exception"""
        if not message:
            message = 'You must activate a valid instance of :class:`environment.Environment`'
        super(EnvironmentInactiveError, self).__init__(message + extra)


class EnvironmentInvalidError(Exception):
    def __init__(self, message=None, extra=''):
        """Exception raised when there is an active instance of :class:`hyperparameter_hunter.environments.Environment`, but it is
        invalid for some reason

        Parameters
        ----------
        message: String, or None, default=None
            A message to provide upon raising `EnvironmentInvalidError`
        extra: String, default=''
            Extra content to append onto the end of `message` before raising the Exception"""
        if not message:
            message = 'The currently active Environment is invalid. Please review proper Environment instantiation'
        super(EnvironmentInvalidError, self).__init__(message + extra)


class RepeatedExperimentError(Exception):
    def __init__(self, message=None, extra=''):
        """Exception raised when a saved Experiment is found with the same hyperparameters as the Experiment being executed

        Parameters
        ----------
        message: String, or None, default=None
            A message to provide upon raising `RepeatedExperimentError`
        extra: String, default=''
            Extra content to append onto the end of `message` before raising the Exception"""
        if not message:
            message = 'An Experiment with identical hyperparameters has already been conducted and has saved results'
        super(RepeatedExperimentError, self).__init__(message + extra)


if __name__ == '__main__':
    pass
