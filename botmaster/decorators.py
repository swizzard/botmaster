"""
Turn functions and generators into twitter bots
"""

import sys
from time import sleep

from twitter import Twitter
from twitter.api import TwitterHTTPError


def parse_err(err):
    """
    Parse a `TwitterHTTPError and extract the error codes from it
    """
    codes = set([error['code'] for error in err.response_data['errors']])
    return codes


def tweet(auth, interval=1800, ignore=None):
    """
    Decorator wrapping a string-returning function that returns
    a function that tweets the results of calling the function
    :param auth: Twitter auth object
    :param interval: how long to wait between tweets
    :param ignore: an optional list of Twitter API error codes to ignore
    """
    def dec(func):
        """
        Wrapper function
        """
        twt = Twitter(auth=auth)
        def inner_dec(*args, **kwargs):
            """
            Inner wrapper
            """
            while True:
                try:
                    twt.statuses.update(status=func(*args, **kwargs))
                except TwitterHTTPError as err:
                    if ignore is None:
                        raise
                    elif not all([(code in ignore) for code in
                                  parse_err(err)]):
                        raise
                else:
                    sleep(interval)
        return inner_dec
    return dec


def gen_tweet(auth, interval=1800, ignore=None, restart=False):
    """
    Decorator wrapping a generator-producing function that
    returns a function that tweets the results of advancing the
    generator
    :param auth: Twitter auth object
    :param interval: how long to wait between tweets
    :param ignore: an optional list of Twitter API error codes to ignore
    :param restart: whether to restart after the generator raises
                    StopIteration
    """
    def dec(func):
        """
        Wrapper function
        """
        twt = Twitter(auth=auth)
        def inner_dec(*args, **kwargs):
            """
            Inner wrapper
            """
            gnr = func(*args, **kwargs)
            while True:
                try:
                    twt.statuses.update(status=(next(gnr)))
                except StopIteration:
                    if restart:
                        gnr = func(*args, **kwargs)
                    else:
                        sys.exit(0)
                except TwitterHTTPError as err:
                    if ignore is None:
                        raise
                    elif not all([(code in ignore) for code in
                                  parse_err(err)]):
                        raise
                else:
                    sleep(interval)
        return inner_dec
    return dec

