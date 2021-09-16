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
from core.api import light
from core.api import glbl
from core.helpers import apply_timezone_datetime
import time
import datetime
import pytz


def main():
    state = _get_state()
    pages = {
        "Home": home,
        "Global": global_settings,
        "Water tank": water_tank_settings,
        "Sprinklers": sprinklers_settings,
        "Uv Lights": lights_settings,
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


def global_settings(state):
    st.title(":wrench: Global Settings")
    r = glbl.get_configuration(GLOBAL_CONFIGURATION)
    if "timezone" in r.keys():
        timezone = st.selectbox(
            "Time Zone",
            pytz.all_timezones,
            index=pytz.all_timezones.index(r["timezone"]),
        )
    else:
        timezone = st.selectbox("Time Zone", pytz.all_timezones)
    if st.button("Save configuration") and glbl.post_configuration(
        GLOBAL_CONFIGURATION,
        {
            "timezone": timezone,
        },
    ):
        st.success("Configuration saved")
        time.sleep(0.5)
        st.experimental_rerun()


def water_tank_settings(state):
    st.title(":droplet: Water tank Settings")
    water_configuration = water.get_configuration(WATER_CONFIGURATION)
    col1, col2 = st.columns(2)
    with col1:
        tds_min_level = st.text_input(
            "Tds min level (ppm)", water_configuration["tds_min_level"]
        )
    with col2:
        tds_max_level = st.text_input(
            "Tds max level (ppm)", water_configuration["tds_max_level"]
        )
    col1, col2 = st.columns(2)
    with col1:
        ph_min_level = st.text_input(
            "pH min level", water_configuration["ph_min_level"]
        )
    with col2:
        ph_max_level = st.text_input(
            "pH max level", water_configuration["ph_max_level"]
        )
    if st.button("Save configuration") and water.post_configuration(
        WATER_CONFIGURATION,
        {
            "tds_min_level": float(tds_min_level),
            "tds_max_level": float(tds_max_level),
            "ph_min_level": float(ph_min_level),
            "ph_max_level": float(ph_max_level),
        },
    ):
        st.success("Configuration saved")
        time.sleep(0.5)
        st.experimental_rerun()

    st.header("Force Actuators")
    force = water.get_configuration(WATER_FORCE_CONTROLLER)
    st.write(force)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Actuators")
        force_water_pump_signal = st.checkbox(
            "Force water pump", value=force["force_water_pump_signal"]
        )
        force_nutrient_pump_signal = st.checkbox(
            "Force nutrient pump", value=force["force_nutrient_pump_signal"]
        )
        force_ph_downer_pump_signal = st.checkbox(
            "Force pH downer pump", value=force["force_ph_downer_pump_signal"]
        )
        force_mixer_pump_signal = st.checkbox(
            "Force water mixer pump", value=force["force_mixer_pump_signal"]
        )
    with col2:
        st.write("True=ON, False=OFF")
        water_pump_signal = st.checkbox(
            "Override water pump ", value=force["water_pump_signal"]
        )
        nutrient_pump_signal = st.checkbox(
            "Override nutrient pump", value=force["nutrient_pump_signal"]
        )
        ph_downer_pump_signal = st.checkbox(
            "Override pH downer pump", value=force["ph_downer_pump_signal"]
        )
        mixer_pump_signal = st.checkbox(
            "Override water mixer pump", value=force["mixer_pump_signal"]
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save"):
            _ = {
                "force_water_pump_signal": force_water_pump_signal,
                "force_nutrient_pump_signal": force_nutrient_pump_signal,
                "force_ph_downer_pump_signal": force_ph_downer_pump_signal,
                "force_mixer_pump_signal": force_mixer_pump_signal,
                "water_pump_signal": water_pump_signal,
                "nutrient_pump_signal": nutrient_pump_signal,
                "ph_downer_pump_signal": ph_downer_pump_signal,
                "mixer_pump_signal": mixer_pump_signal,
            }
            if water.post_configuration(WATER_FORCE_CONTROLLER, _):
                st.success("Successfully Forced")
                st.experimental_rerun()
    with col2:
        if st.button("Reset"):
            _ = {
                "force_water_pump_signal": False,
                "force_nutrient_pump_signal": False,
                "force_ph_downer_pump_signal": False,
                "force_mixer_pump_signal": False,
                "water_pump_signal": False,
                "nutrient_pump_signal": False,
                "ph_downer_pump_signal": False,
                "mixer_pump_signal": False,
            }
            if water.post_configuration(WATER_FORCE_CONTROLLER, _):
                st.success("Successfully reset")
                st.experimental_rerun()


def sprinklers_settings(state):
    """
    TODO: reduce cognitive complexity
    """
    st.title(":potable_water: Sprinklers Settings")
    st.header("Create new sprinkler / configure existing")
    sprinklers_tag_list: list = sprinklers.get_tags(SPRINKLER_REGISTRY)

    if sprinklers_tag_list:
        sprinkler = st.radio("Available sprinkler(s) ", sprinklers_tag_list)
        sprinkler_config = sprinklers.get_configuration(
            SPRINKLER_CONFIGURATION, sprinkler
        )
    else:
        sprinkler = st.radio(
            "Available sprinkler(s) ", ["not tag found, create a tag "]
        )
        sprinkler_config = {
            "soil_moisture_min_level": 20.0,
            "soil_moisture_max_level": 70.0,
        }

    tag = st.text_input("Add new tag / configure existing", sprinkler)
    col1, col2 = st.columns(2)
    with col1:
        min_moisture = st.text_input(
            "Minimum moisture level", sprinkler_config["soil_moisture_min_level"]
        )
    with col2:
        max_moisture = st.text_input(
            "Maximum moisture level", sprinkler_config["soil_moisture_max_level"]
        )
    if st.button("(Create tag and) save sprinkler settings"):
        tag_result = sprinklers.create_tag(SPRINKLER_REGISTRY, tag)
        configuration_result = sprinklers.post_configuration(
            SPRINKLER_CONFIGURATION,
            tag,
            config={
                "soil_moisture_min_level": float(min_moisture),
                "soil_moisture_max_level": float(max_moisture),
            },
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

    st.header("Delete existing tag and configuration")
    confirm_delete = st.text_input("To delete confirm by writing sprinkler tag here")
    if st.button("Delete this sprinkler"):
        if sprinkler == confirm_delete:
            if sprinklers.delete_tag(SPRINKLER_REGISTRY, sprinkler):
                st.success("Successfully Delete")
                st.experimental_rerun()
            else:
                st.warning("Can not delete this tag: maybe already deleted")
        else:
            st.error(
                "Please select good tag and confirm deletion by writing sprinkler tag"
            )
    st.header("Force Water Valve")
    force = sprinklers.get_configuration(SPRINKLER_FORCE_CONTROLLER, sprinkler)
    col1, col2 = st.columns(2)
    with col1:
        force_water_valve_signal = st.checkbox(
            "Force Status", value=force["force_water_valve_signal"]
        )
    with col2:
        water_valve_signal = st.checkbox(
            "Override (True=ON, False=OFF)", value=force["water_valve_signal"]
        )

    col1, col2 = st.columns(2)
    post_response = {"type": "not_set", "status": False}
    with col1:
        if st.button("Save"):
            _ = {
                "force_water_valve_signal": force_water_valve_signal,
                "water_valve_signal": water_valve_signal,
            }
            if sprinklers.post_controller_force(
                SPRINKLER_FORCE_CONTROLLER, sprinkler, _
            ):
                post_response["type"] = "config"
                post_response["status"] = True

    with col2:
        if st.button("Reset"):
            _ = {"force_water_valve_signal": False, "water_valve_signal": False}
            if sprinklers.post_controller_force(
                SPRINKLER_FORCE_CONTROLLER, sprinkler, _
            ):
                post_response["type"] = "reset"
                post_response["status"] = True

    if post_response["status"]:
        if post_response["type"] == "config":
            st.success("Successfully Forced")
        elif post_response["type"] == "reset":
            st.success("Successfully force reset")
        time.sleep(0.5)
        st.experimental_rerun()


def lights_settings(state):
    """
    TODO: reduce cognitive complexity
    """
    st.title(":bulb: UV Light Settings")
    try:
        timezone = glbl.get_configuration(GLOBAL_CONFIGURATION)["timezone"]
    except KeyError:
        st.error('Timezone is not configured, configure it "Gobal" > "Time zone" first')
    else:
        st.write("Time zone:", timezone)

    st.header("Create new light / configure existing")
    lights_tag_list: list = light.get_tags(LIGHT_REGISTRY)

    if lights_tag_list:
        _light = st.radio("Available light(s) ", lights_tag_list)
        light_config = light.get_configuration(LIGHT_CONFIGURATION, _light)
    else:
        _light = st.radio("Available light(s) ", ["not tag found, create a tag "])
        light_config = {
            "on_datetime_at": datetime.time(8, 0),
            "off_datetime_at": datetime.time(18, 0),
        }

    tag = st.text_input("Add new tag / configure existing", _light)
    col1, col2 = st.columns(2)

    with col1:
        on_time_at = st.time_input("Light on from", light_config["on_datetime_at"])
    with col2:
        off_time_at = st.time_input("Light on to", light_config["off_datetime_at"])

    tz_on_time_at = apply_timezone_datetime(timezone, on_time_at)
    tz_off_time_at = apply_timezone_datetime(timezone, off_time_at)

    if st.button("(Create tag and) save light settings"):
        tag_result = light.create_tag(LIGHT_REGISTRY, tag)
        configuration_result = light.post_configuration(
            LIGHT_CONFIGURATION,
            tag,
            config={"on_datetime_at": tz_on_time_at, "off_datetime_at": tz_off_time_at},
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

    st.header("Delete existing tag and configuration")
    confirm_delete = st.text_input("To delete confirm by writing sprinkler tag here")
    if st.button("Delete this light"):
        if _light == confirm_delete:
            if light.delete_tag(LIGHT_REGISTRY, _light):
                st.success("Successfully Delete")
                st.experimental_rerun()
            else:
                st.warning("Can not delete this tag: maybe already deleted")
        else:
            st.error("Please select good tag and confirm deletion by writing light tag")


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
            if self._state["hash"] != self._state["hasher"].to_bytes(
                self._state["data"], None
            ):
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
