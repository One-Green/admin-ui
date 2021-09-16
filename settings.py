import os

ONE_GREEN_API_URL: str = os.getenv("ONE_GREEN_API_URL")
API_BASIC_AUTH_USERNAME: str = os.getenv("API_BASIC_AUTH_USERNAME")
API_BASIC_AUTH_PASSWORD: str = os.getenv("API_BASIC_AUTH_PASSWORD")
BASIC_AUTH: tuple = (API_BASIC_AUTH_USERNAME, API_BASIC_AUTH_PASSWORD)

GLOBAL_CONFIGURATION: str = os.path.join(ONE_GREEN_API_URL, "global/config")

WATER_CONFIGURATION: str = os.path.join(ONE_GREEN_API_URL, "water/config")
WATER_FORCE_CONTROLLER: str = os.path.join(ONE_GREEN_API_URL, "water/controller/force")

SPRINKLER_REGISTRY: str = os.path.join(ONE_GREEN_API_URL, "sprinkler/registry")
SPRINKLER_CONFIGURATION: str = os.path.join(ONE_GREEN_API_URL, "sprinkler/config")
SPRINKLER_FORCE_CONTROLLER: str = os.path.join(
    ONE_GREEN_API_URL, "sprinkler/controller/force"
)

LIGHT_REGISTRY: str = os.path.join(ONE_GREEN_API_URL, "light/registry")
LIGHT_CONFIGURATION: str = os.path.join(ONE_GREEN_API_URL, "light/config")
