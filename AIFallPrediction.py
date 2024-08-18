#Filename: AIFallPrediction1.py
# Objective: AI HealthCare Fall Prediction Analytics Application.
# Remarks:
# Developer: Mr Michael Tan Kok Liang
# Date: 12/08/2024

# PYTHONIC LIBRARIES
# -------------------cls
import streamlit as st;
import streamlit_authenticator as stauth;
import pandas as pd;
import json;
import cx_Freeze, sys;
from st_on_hover_tabs import on_hover_tabs;

#---------------- USER CREDENTIALS CONFIGURATIONS --------------------------
import yaml;
from yaml.loader import SafeLoader;
# ===========================================================================

# -----------------------------  GLOBAL VARIABLES -----------------------------------
global today, now, current_weekday, current_weekday_datetime, d1, d2, d3, pathname, frames, timer1_running;
global pageTitle, pageIcon, pageLayout, pageSidebar, docHeader, docIcon, docMenuItems, healthCareImage, securityAccessImage;
global docSubHeader, homePageInfo;
# ======================================================================================

def setConfig(): # Reads JSON configuration file and setup Streamlit application accordingly.
    # Reading JSON Configuration File
    # ----------------------------------
    with open('data\\Config.json') as user_file:
        file_contents = user_file.read();
        parsed_json = json.loads(file_contents);  # Parse JSON File Contents

        # Extract out respective JSON file parameters
        # --------------------------------------------
        pageTitle = parsed_json["stlit_page_title"];  # Extracts the page's title information.
        pageIcon = parsed_json["stlit_page_icon"];  # Extracts the page's icon information.
        pageLayout = parsed_json["stlit_page_layout"];  # Extracts the page's layout information.
        pageSidebar = parsed_json["stlit_initial_sidebar_state"];  # Extracts the page's sidebar information.
        docHeader = parsed_json["stlit_doc_header"];  # Extracts the page document's header information.
        docSubHeader = parsed_json["stlit_doc_subheader"];  # Extracts the page document's SubHeader information.
        docIcon = parsed_json["stlit_doc_icon"];  # Extracts the page document's icon picture.
        docMenuItems = parsed_json["stlit_menu_items"];  # Extracts the page document's menu items information.
        healthCareImage = parsed_json["stlit_Healtcare_image"];  # Extracts the page document's healthcare image picture information.
        healthCareImageWidth = parsed_json["stlit_Healtcare_image_width"];  # Extracts the page document's healthcare image picture's width information.
        securityAccessImage = parsed_json["stlit_Security_image"];  # Extracts the login page Security Login image picture information.
        securityAccessImageWidth = parsed_json["stlit_Security_image_width"];  # Extracts the login page Security Login image picture's width information.
        #docMenuItems = parsed_json["stlit_menu_items"];  # Extracts the page document's menu items information.
        homePageInfo = parsed_json["stlit_home_page_info"];  # Extracts the home page document information.
        footerPageInfo = parsed_json["stlit_footer_page_info"];  # Extracts the footer page document information.

        # Sets the Streamlit Application Configuration
        # ---------------------------------------------
        st.set_page_config(page_title=pageTitle, page_icon=pageIcon, layout=pageLayout,
                           initial_sidebar_state=pageSidebar, menu_items=None);

        # Importing stylesheet
        st.markdown('<style>' + open("st_on_hover_tabs/style.css").read() + '</style>', unsafe_allow_html=True);

    return docHeader, docSubHeader, docIcon, healthCareImage, healthCareImageWidth, securityAccessImage, securityAccessImageWidth, homePageInfo, footerPageInfo;

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8');

def readUserCredentials(): # Reads YAML User Credentials Configuration File.
    with open('data\\Credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader);

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['pre-authorized']
        );

        return authenticator;
def signIn(securityAccessImage, securityAccessImageWidth, authenticator): # Displays the login widget.

    # Displays a centralized image
    # ------------------------------
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image(f"{securityAccessImage}", width=securityAccessImageWidth); # Displays the Security Login Image picture.

    authenticator.login("main"); # Displays the login widget.
def authenticateUser(docHeader, docSubHeader, docIcon, healthCareImage, healthCareImageWidth, homepageInfo,
                     authenticator, footerPageInfo):  # Authenticates Authorized Users
    if st.session_state['authentication_status']:
        #test=authenticator.logout("Logout","sidebar");

        # Displays a Welcome greeting message for authorized login user.
        #----------------------------------------------------------------
        st.write(f'Welcome *{st.session_state["name"]}*');

        # Displays a centralized image
        # ------------------------------
        left_co, cent_co, last_co = st.columns(3)
        with cent_co:
            st.image(f"{healthCareImage}", width=healthCareImageWidth);  # Displays the Security Login Image picture.

        uploaded_files = st.file_uploader("Choose Health Record File", accept_multiple_files=True);

        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read();
            st.write(f"Dataset Source Loaded Successfully -> Filename: {uploaded_file.name}");
            # st.write(bytes_data)

            # print(f"Selected Filename: {uploaded_file.name}");

            # Displays the contents of the CSV file
            # ----------------------------------------
            df = pd.read_csv(uploaded_file.name);

            st.dataframe(df);

            csv = convert_df(df);

            st.download_button(
                "Download Data",
                csv,
                "file.csv",
                "text/csv",
                key='download-csv'
            );

       # Sidebar Navigation
       #--------------------
        with st.sidebar:
            tabs = on_hover_tabs(tabName=['Dashboard', 'About', 'Contact'],
                                 iconName=['dashboard', 'info', 'mail']);

        if tabs == 'Dashboard':
            #pass
            st.switch_page("pages/AIFallPrediction.py");  # Navigates to the dashboard subpage.

        elif tabs == 'About': # Sub-page still under development.
            st.info("An Innovative AI Healthcare Project.");

        elif tabs == 'Contact': # Sub-page still under development.
            st.warning("Please contact the app developer at: coloss323@gmail.com");

        st.write("");
        st.write("");

        test = authenticator.logout("Logout", "sidebar");

        #st.rerun();

    if st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect');
    if st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password');

    st.html(
        "<p><h5><center>An AI Healthcare Solution Project. Proudly developed with ❤️ using Streamlit. 😎</center></h5></p>"
    )

if __name__ == "__main__":
    docHeader, docSubHeader, docIcon, healthCareImage, healthCareImageWidth, securityAccessImage, securityAccessImageWidth, homepageInfo, footerPageInfo = setConfig();  # Requqests for service to set the page's configuration.
    authenticator = readUserCredentials();  # Requests for service to read the YAML User Credentials Configuration File.
    signIn(securityAccessImage, securityAccessImageWidth,authenticator);  # Requests for service to display the login widget.
    authenticateUser(docHeader, docSubHeader, docIcon, healthCareImage, healthCareImageWidth, homepageInfo,authenticator, footerPageInfo);  # Requests for service to authenticate all authorized users.
