import streamlit as st
from app_tabs.about import about_matrix
from app_tabs.when_to_use import when_to_use
from app_tabs.how_to_use import how_to_use
from app_tabs.mfa import mfa_tool

# Set page config, title, icon, etc
st.set_page_config(
    page_title="MFA", 
    page_icon=":deciduous_tree:", 
    layout="wide",
    initial_sidebar_state="collapsed")

# Title set using markdown
st.markdown("<h1 style='text-align: center; color: black;'>Multifuntionality potential and cost assessment</h1>", unsafe_allow_html=True)

# Inject CSS to center the tab headers
st.markdown(
    """
    <style>
    
    /* Target the tab header container */
    .stTabs [role="tablist"] {
        justify-content: center;
    }
    
    /* Target all tab labels */
    .stTabs [role="tab"] p {
        font-size: 20px !important;
        font-weight: bold !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Create tabs on top of page
tab1, tab2, tab3 = st.tabs([
                            'Multifuntionality potential and cost matrix',
                            'How to use the matrix',
                            'About the matrix',
])

# What each tab should contain. The functions are in the scripts in the app_tabs directory.
with tab1:
    mfa_tool()

with tab2:
    how_to_use()

with tab3:
    about_matrix()

# with tab3:
    #when_to_use()

