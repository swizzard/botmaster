from os import getenv
from time import sleep

from twitter import Twitter
from twitter.oauth import OAuth


def _auth(access_token, access_secret, api_key, api_secret):
  """
  Create a `twitter.OAuth` object from strings
  """
    return OAuth(access_token, access_secret, api_key, api_secret)


def env_auth(access_token_var="access_token",
             access_secret_var="access_secret",
             api_key_var="api_key",
             api_secret_var="api_secret"):
    """
    Create a `twitter.OAuth` object from environment variables
    """
    return OAuth(getenv(access_token_var),
                       getenv(access_secret_var),
                       getenv(api_key_var),
                       getenv(api_secret_var))


def tweet(auth=env_auth(), interval=1800):
    def dec(f):
        t = Twitter(auth=auth)
        def inner_dec(*args, **kwargs):
            while True:
                t.statuses.update(status=f(*args, **kwargs))
        return inner_dec
    return dec


def gen_tweet(auth=env_auth(), interval=1800):
    def dec(f):
        t = Twitter(auth=auth)
        def inner_dec(*args, **kwargs):
            g = f(*args, **kwargs)
            while True:
                try:
                    t.statuses.update(status=g.next())
                    sleep(1800)
                except StatusIteration:
                    sys.exit(0)
