"""
Turn functions and generators into twitter bots
"""

from os import getenv
import sys
from time import sleep

from twitter import Twitter
from twitter.oauth import OAuth


def _auth(access_token, access_secret, api_key, api_secret):
    """
    Create a `twitter.OAuth` object from strings
    :param access_token: Twitter OAuth access token
    :param access_secret: Twitter OAuth access secret
    :param api_key: Twitter OAuth api key
    :param api_secret: Twitter OAuth api secret
    """
    return OAuth(access_token, access_secret, api_key, api_secret)


def env_auth(access_token_var="access_token",
             access_secret_var="access_secret",
             api_key_var="api_key",
             api_secret_var="api_secret"):
    """
    Create a `twitter.OAuth` object from environment variables
    :param access_token_var: name of environment variable holding Twitter
                             OAuth access token
    :param access_secret_var: name of environment variable holding Twitter
                              OAuth access secret
    :param api_key_var: name of environment variable holding Twitter
                        OAuth API key
    :param api_secret_var:  name of environment variable holding Twitter
                            OAuth API secret
    """
    return OAuth(getenv(access_token_var),
                 getenv(access_secret_var),
                 getenv(api_key_var),
                 getenv(api_secret_var))


def tweet(auth, interval=1800):
    """
    Decorator wrapping a string-returning function that returns
    a function that tweets the results of calling the function
    :param auth: Twitter auth object
    :param interval: how long to wait between tweets
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
                twt.statuses.update(status=func(*args, **kwargs))
                sleep(interval)
        return inner_dec
    return dec


def gen_tweet(auth=env_auth(), interval=1800):
    """
    Decorator wrapping a generator-producing function that
    returns a function that tweets the results of advancing the
    generator
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
                    twt.statuses.update(status=gnr.next())
                    sleep(interval)
                except StopIteration:
                    sys.exit(0)
        return inner_dec
    return dec

