import streamlit as st
import os
import json
import traceback
import logging
from azure.cosmos import CosmosClient
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)
st.set_page_config(page_title="Explore Data", page_icon=os.path.join('images','favicon.ico'), layout="wide", menu_items=None)
mod_page_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(mod_page_style, unsafe_allow_html=True)

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

try:
    # Initialize Cosmos Client
    url = os.environ['COSMOSDB_ENDPOINT']
    key = os.environ['COSMOSDB_KEY']
    client = CosmosClient(url, credential=key)

    # Get database
    database_name = os.environ['COSMOSDB_DBNAME']
    database = client.get_database_client(database_name)

    # Get container names
    container_names = [container['id'] for container in database.list_containers()]

    # Create a dropdown menu for container names
    container_name = st.selectbox('Select an RFP document source:', container_names)

    if container_name:
        # Get the data for the selected container
        container = database.get_container_client(container_name)
        items = list(container.read_all_items(max_item_count=100))  # limit to 100 items for demo

        # Create a dropdown menu for item names
        item_names = [item['id'] for item in items]
        item_name = st.selectbox('Select an RFP doc:', item_names)

        if item_name:
            # Find the selected item
            selected_item = next((item for item in items if item['id'] == item_name), None)

            # Display the selected item in a friendly view
            st.json(selected_item)

            # Create an expandable section for "Extract questions"
            with st.expander('Extract and review questions'):
                if st.button('Extract questions'):
                    # Code to extract questions goes here
                    st.write('Questions extracted.')

            # Create an expandable section for "Generate answers"
            with st.expander('Generate answers and evaluate their accuracy'):
                if st.button('Generate answers'):
                    # Code to generate answers goes here
                    st.write('Answers generated.')

except Exception as e:
    st.error(traceback.format_exc())