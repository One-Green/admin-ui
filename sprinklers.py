from settings import *
from core.api import sprinklers
import streamlit as st

st.title("Sprinklers Configuration")

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

tag = st.text_input("Add new tag", sprinkler)
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
        st.success("Tag created")
    if configuration_result:
        st.success("Configuration saved")
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
            st.success("Delete successfully")
        else:
            st.warning("Can not delete this tag: maybe already deleted")
    else:
        st.error("Please confirm deletion by writing sprinkler tag")
