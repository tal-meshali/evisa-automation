import os

from api.countries.india.consts.referer import Referer
from api.countries.india.consts.urls import BASE_URL, URL_CHAIN


def get_current_url(url: str):
    return os.path.join(BASE_URL, url)


def get_referer_url(url: str, referer: Referer):
    referer = URL_CHAIN[URL_CHAIN.index(url) - referer.value]
    return os.path.join(BASE_URL, referer)
