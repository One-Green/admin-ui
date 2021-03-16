import os

ONE_GREEN_CORE_API: str = os.getenv("ONE_GREEN_CORE_API")
API_BASIC_AUTH_USERNAME: str = os.getenv("API_BASIC_AUTH_USERNAME")
API_BASIC_AUTH_PASSWORD: str = os.getenv("API_BASIC_AUTH_PASSWORD")
BASIC_AUTH: tuple = (API_BASIC_AUTH_USERNAME, API_BASIC_AUTH_PASSWORD)

GLOBAL_CONFIGURATION: str = os.path.join(ONE_GREEN_CORE_API, "global/config")

WATER_CONFIGURATION: str = os.path.join(ONE_GREEN_CORE_API, "water/config")
WATER_FORCE_CONTROLLER: str = os.path.join(ONE_GREEN_CORE_API, "water/controller/force")

SPRINKLER_REGISTRY: str = os.path.join(ONE_GREEN_CORE_API, "sprinkler/registry")
SPRINKLER_CONFIGURATION: str = os.path.join(ONE_GREEN_CORE_API, "sprinkler/config")
SPRINKLER_FORCE_CONTROLLER: str = os.path.join(ONE_GREEN_CORE_API, "sprinkler/controller/force")

LIGHT_REGISTRY: str = os.path.join(ONE_GREEN_CORE_API, "light/registry")
LIGHT_CONFIGURATION: str = os.path.join(ONE_GREEN_CORE_API, "light/config")
