"""
Auth stuff for botmaster
"""
from os import getenv

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

