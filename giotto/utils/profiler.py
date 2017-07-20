#-*- coding: utf-8 -*-
""" Collection of classes for profiling.

This module defines easy-to-use tools for function-level performance profiling.
We implement function-level profiling tool as a function decorator. To ease the
processing of profile records, we use standard python `logging` to log each
data record.

"""

import time
import logging
import unittest


class Profiler:
    """ Base class for Profilers.

    This class serves as a base flass for all profile classes whose profiling
    tools were implemented as decorators.

    Note:
        Each decorator may be implemented by overriding the base classmethod
        `profile`.

    """

    @classmethod
    def profile(cls, logger=None):
        """ Base profile decorator.

        This base profile decorator does nothing but returning the original
        function it is decorating.

        Note:
            This profile decorator would be overriden by subclass profilers.

        Args:
            logger (:obj:`logging.Logger`, optional): a logger where the
                profiler records the measurements.

        """

        def profile_decorator(func):
            def func_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return func_wrapper
        return profile_decorator


class SimpleProfiler(Profiler):
    """ Simple profiler that records function entry and exit time. """
    @classmethod
    def profile(cls, logger=None):
        """ Simple profile decorator.

        This simple profile decorator records the elapsed time between
        the function entry and exit. This decorator overrides the decorator
        of the base class `Profiler`.

        Args:
            logger (:obj:`logging.Logger`, optional): a logger where the
                profiler records the measurements.

        """
        def profile_decorator(func):
            if logger is None:
                return func
            else:
                def func_wrapper(*args, **kwargs):
                    start_time = time.time()
                    func_return = func(*args, **kwargs)
                    time_span = time.time() - start_time
                    msg = '{} {} {}'.format(func.__module__,
                                            func.__name__,
                                            time_span)
                    logger.debug(unicode(msg))
                    return func_return
                return func_wrapper
        return profile_decorator


class SimpleProfilerTest(unittest.TestCase):
    """ Unittest for SimpleProfiler class.

    This class defines a simple unittest on SimpleProfiler. It creates a
    logger with `io.StringIO` stream. It checks whether the decorator is
    recording the function properly.

    """
    def setUp(self):
        """ Setup a stream logger to get the decorator output. """
        # setup a stream and its handler
        from io import StringIO
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)

        # setup a logger and set the level as DEBUG
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # register the handler and deletes all other handlers
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        """ Destroys the logger and stream after performing tests. """
        # deregister the handler and close the stream
        self.logger.removeHandler(self.handler)
        self.handler.close()

    def test_performance_logging(self):
        """ Tests basic function of the decorator. """
        # A simple function that sleeps for a second
        @SimpleProfiler.profile(self.logger)
        def test_function():
            start_time = time.time()
            time.sleep(1)
            return (time.time() - start_time)

        # get the timespan the function was running
        func_time = test_function()

        # flush to the stream
        self.handler.flush()

        # get the time recored by the logger
        decorator_time = float(self.stream.getvalue().split()[-1])

        # assert the decorator-recorded time is longer than the time recorded
        # by the function.
        assert func_time < decorator_time


if __name__ == '__main__':
    unittest.main()
