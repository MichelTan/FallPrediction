# Filename: dashboard.py

# PYTHONIC LIBRARY
#------------------
import streamlit as st;
import streamlit_authenticator as stauth;
from st_on_hover_tabs import on_hover_tabs;

#---------------- USER CREDENTIALS CONFIGURATIONS --------------------------
import yaml;
from yaml.loader import SafeLoader;
# ===========================================================================

global authenticator;

st.set_page_config(layout="wide");
def readConfig(): # Reads YAML Configuration File.
    with open('Credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader);

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['pre-authorized']
        );

        return authenticator;

def setConfig(authenticator):
    #st.set_page_config(layout="wide");

    # Importing stylesheet
    st.markdown('<style>' + open("st_on_hover_tabs/style.css").read() + '</style>', unsafe_allow_html=True);

    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Dashboard', 'About', 'Contact'],
                         iconName=['dashboard', 'info', 'mail'], default_choice=0);

    st.title("Navigation Bar");
    st.write('Name of option is {}'.format(tabs));

    if st.session_state['authentication_status']:
        st.write("");
        st.write("");
        test = authenticator.logout("Logout", "sidebar");
    if st.session_state['authentication_status'] is None:
        st.switch_page("AIFallPrediction1.py");  # Navigates to the dashboard subpage.
        st.warning('Please enter your username and password');

if __name__ == "__main__":
    authenticator = readConfig();
    setConfig(authenticator);
