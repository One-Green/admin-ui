"""
One-green IoT ui admin
multi page agg based on template: https://discuss.streamlit.io/t/multi-page-app-with-session-state/3074

Author: Shanmugathas Vigneswaran
Mail: shanmugathas.vigneswaran@outlook.fr
"""
import streamlit as st
from streamlit.hashing import _CodeHasher
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server
from settings import *
from core.api import sprinklers
from core.api import water
import time


def main():
    state = _get_state()
    pages = {
        "Home": home,
        "Water tank": water_tank_settings,
        "Sprinklers": sprinklers_settings,
        # "Uv Light": lights_settings,
        # "Air temperature": air_settings,
        # "Air humidity": air_humidity
    }
    st.sidebar.image("_static/logo.png")
    st.sidebar.title(":wrench: Admin")
    page = st.sidebar.radio("Select which page to go", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


def home(state):
    st.title("One-Green Admin")
    st.header("Place to configure your IoT devices handled by One-Green Core")


def water_tank_settings(state):
    st.title(":droplet: Water tank Settings")
    water_configuration = water.get_configuration(WATER_CONFIGURATION)
    tds_min_level = st.text_input("Tds min level (ppm)", water_configuration["tds_min_level"])
    tds_max_level = st.text_input("Tds max level (ppm)", water_configuration["tds_max_level"])
    ph_min_level = st.text_input("pH min level", water_configuration["ph_min_level"])
    ph_max_level = st.text_input("pH max level", water_configuration["ph_max_level"])
    if st.button("Save configuration") and water.post_configuration(
            WATER_CONFIGURATION,
            {
                "tds_min_level": float(tds_min_level),
                "tds_max_level": float(tds_max_level),
                "ph_min_level": float(ph_min_level),
                "ph_max_level": float(ph_max_level)
            }
    ):
        st.success("Configuration saved")
        time.sleep(0.5)
        st.experimental_rerun()


def sprinklers_settings(state):
    st.title(":potable_water: Sprinklers Settings")
    st.header('Create new sprinkler / configure existing')
    sprinklers_tag_list: list = sprinklers.get_tags(SPRINKLER_REGISTRY)

    if sprinklers_tag_list:
        sprinkler = st.radio('Available sprinkler(s) ', sprinklers_tag_list)
        sprinkler_config = sprinklers.get_configuration(SPRINKLER_CONFIGURATION, sprinkler)
    else:
        sprinkler = st.radio('Available sprinkler(s) ', ["not tag found, create a tag "])
        sprinkler_config = {
            "soil_moisture_min_level": 20.,
            "soil_moisture_max_level": 70.
        }

    tag = st.text_input("Add new tag / configure existing", sprinkler)
    min_moisture = st.text_input("Minimum moisture level", sprinkler_config["soil_moisture_min_level"])
    max_moisture = st.text_input("Maximum moisture level", sprinkler_config["soil_moisture_max_level"])
    if st.button("Create tag and save sprinkler settings"):
        tag_result = sprinklers.create_tag(SPRINKLER_REGISTRY, tag)
        configuration_result = sprinklers.post_configuration(
            SPRINKLER_CONFIGURATION,
            tag,
            config={
                "soil_moisture_min_level": float(min_moisture),
                "soil_moisture_max_level": float(max_moisture)
            }
        )
        if tag_result:
            time.sleep(0.5)
            st.success("Tag created")
        if configuration_result:
            time.sleep(0.5)
            st.success("Configuration saved")
            st.experimental_rerun()
        else:
            st.error("Can not save this configuration")

    st.header('Delete existing tag and configuration')
    confirm_delete = st.text_input("To delete confirm by writing sprinkler tag here")
    if st.button("Delete this sprinkler"):
        if sprinkler == confirm_delete:
            if sprinklers.delete_tag(
                    SPRINKLER_REGISTRY,
                    sprinkler
            ):
                st.success("Successfully Delete")
                st.experimental_rerun()
            else:
                st.warning("Can not delete this tag: maybe already deleted")
        else:
            st.error("Please select good tag and confirm deletion by writing sprinkler tag")


# def lights_settings(state):
#     st.title("UV Light settings")
#
#
# def air_settings(state):
#     st.title("Air temperature settings")
#
#
# def air_humidity(state):
#     st.title("Air humidity settings")


class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state


if __name__ == "__main__":
    main()
