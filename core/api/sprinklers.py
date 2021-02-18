import os
import requests
from json.decoder import JSONDecodeError


def create_tag(api: str, tag=str, _basic_auth: tuple = None) -> bool:
    """
    Create new sprinkler tag by api
    :param api:
    :param tag:
    :param _basic_auth:
    :return:
    """
    if _basic_auth:
        if requests.post(api, data={"tag": tag}, basic_auth=_basic_auth).json()['acknowledge']:
            return True
        else:
            return False
    else:
        if requests.post(api, data={"tag": tag}).json()['acknowledge']:
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
        if requests.delete(api, data={"tag": tag}, basic_auth=_basic_auth).ok:
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
        return requests.get(api, basic_auth=_basic_auth).json()
    else:
        return requests.get(api).json()


def get_configuration(
        api: str,
        sprinkler_tag: str,
        _basic_auth: tuple = None
) -> dict:
    """
    Configure a sprinkler with is tag
    :param api:
    :param sprinkler_tag:
    :param config:
    :param _basic_auth:
    :return:
    """
    _api = os.path.join(api, sprinkler_tag)
    try:
        if _basic_auth:
            return requests.get(_api, basic_auth=_basic_auth).json()
        else:
            return requests.get(_api).json()
    except JSONDecodeError:
        return {
            "soil_moisture_min_level": "not set",
            "soil_moisture_max_level": "not set"
        }


def post_configuration(
        api: str,
        sprinkler_tag: str,
        config: dict,
        _basic_auth: tuple = None
) -> bool:
    """
    Configure a sprinkler with is tag
    :param api:
    :param sprinkler_tag:
    :param config:
    :param _basic_auth:
    :return:
    """
    _api = os.path.join(api, sprinkler_tag)

    if _basic_auth:
        if requests.post(_api, json=config, basic_auth=_basic_auth).ok:
            return True
        else:
            return False
    else:
        if requests.post(_api, json=config).ok:
            return True
        else:
            return False
