import os
import requests
from json.decoder import JSONDecodeError
import datetime
from dateutil import parser
from core.api import glbl
from settings import GLOBAL_CONFIGURATION
import pytz


def create_tag(api: str, tag=str, _basic_auth: tuple = None) -> bool:
    """
    Create new sprinkler tag by api
    :param api:
    :param tag:
    :param _basic_auth:
    :return:
    """
    if _basic_auth:
        if requests.post(api, data={"tag": tag}, auth=_basic_auth).json()[
            "acknowledge"
        ]:
            return True
        else:
            return False
    else:
        if requests.post(api, data={"tag": tag}).json()["acknowledge"]:
            return True
        else:
            return False


def delete_tag(api: str, tag=str, _basic_auth: tuple = None) -> bool:
    """
    Delete sprinklers tags by api
    :param api:
    :param tag:
    :param _basic_auth:
    :return:
    """

    if _basic_auth:
        if requests.delete(api, data={"tag": tag}, auth=_basic_auth).ok:
            return True
        else:
            return False
    else:
        if requests.delete(api, data={"tag": tag}).ok:
            return True
        else:
            return False


def get_tags(api: str, _basic_auth: tuple = None) -> list:
    """
    Get sprinklers tags by api
    :param api:
    :param _basic_auth:
    :return:
    """
    if _basic_auth:
        return requests.get(api, auth=_basic_auth).json()
    else:
        return requests.get(api).json()


def get_configuration(api: str, _tag: str, _basic_auth: tuple = None) -> dict:
    """
    Configure a sprinkler with is tag
    :param api:
    :param _tag:
    :param _basic_auth:
    :return:
    """
    _api = os.path.join(api, _tag)
    timezone = glbl.get_configuration(GLOBAL_CONFIGURATION)["timezone"]

    try:
        if _basic_auth:
            r = requests.get(_api, auth=_basic_auth).json()
        else:
            r = requests.get(_api).json()
        r["on_datetime_at"] = parser.parse(r["on_datetime_at"]).astimezone(
            pytz.timezone(timezone)
        )
        r["off_datetime_at"] = parser.parse(r["off_datetime_at"]).astimezone(
            pytz.timezone(timezone)
        )
    except JSONDecodeError:
        r = {
            "on_datetime_at": datetime.time(0, 0),
            "off_datetime_at": datetime.time(0, 0),
        }
    return r


def post_configuration(
    api: str, _tag: str, config: dict, _basic_auth: tuple = None
) -> bool:
    """
    Configure a sprinkler with is tag
    :param api:
    :param _tag:
    :param config:
    :param _basic_auth:
    :return:
    """
    _api = os.path.join(api, _tag)
    config["on_datetime_at"]: datetime.datetime = config["on_datetime_at"].isoformat()
    config["off_datetime_at"]: datetime.datetime = config["off_datetime_at"].isoformat()
    if _basic_auth:
        if requests.post(_api, json=config, auth=_basic_auth).ok:
            return True
        else:
            return False
    else:
        if requests.post(_api, json=config).ok:
            return True
        else:
            return False
