import requests


def get_configuration(api: str, _basic_auth: tuple = None) -> dict:
    """
    Configure water tank
    :param api:
    :param _basic_auth:
    :return:
    """
    if _basic_auth:
        return requests.get(api, auth=_basic_auth).json()
    else:
        return requests.get(api).json()


def post_configuration(api: str, config: dict, _basic_auth: tuple = None) -> bool:
    """
    Configure a sprinkler with is tag
    :param api:
    :param config:
    :param _basic_auth:
    :return:
    """

    if _basic_auth:
        if requests.post(api, json=config, auth=_basic_auth).json()[
            "acknowledge"
        ]:
            return True
        else:
            return False
    else:
        if requests.post(api, json=config).json()["acknowledge"]:
            return True
        else:
            return False
