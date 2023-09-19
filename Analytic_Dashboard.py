import tempfile
import time
import streamlit as st
from settings import *
from streamlit_lottie import st_lottie
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import yaml
from yaml.loader import SafeLoader

# streamlit run Analytic_Dashboard.py

st.set_page_config(page_title=TITLE,
    page_icon=PAGE_ICON,
    layout="wide")


with open(config_Dash) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

with open(css_file) as f: # Load the CSS file
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.markdown("<h2 style=\
    'text-align : center';\
    font-weight : bold ;\
    font-family : Arial;>\
    Analytic Dashboard</h2>", unsafe_allow_html=True)

st.markdown("""---""")

with st.sidebar :
    clickable_img_logo = get_img_with_href(pp_logo_portfolio, 'https://ybouhlal.streamlit.app/', 70, "blank")
    st.markdown(clickable_img_logo, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    clickable_img = get_img_with_href(linkpic_code, 'https://github.com/bouhlalyassine/Analytic_Dashboard',
        170, "blank")
    st.markdown(clickable_img, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    nav_menu = option_menu(menu_title=None, options=['Home', 'Example APP'], 
        default_index=0, orientation="vertical",
        icons=["house", "app"],
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"2px", "--hover-color": "#805E83"}
        })



if nav_menu == 'Home':
    st.markdown("<br>", unsafe_allow_html=True)

    colpi1, colpi2 = st.columns([75, 25], gap="small")
    with colpi1:
        st.info("Analytic Dashboard, is a simple example of a data analysis webapp that allows you to :\
            \n ● Automate data processing\
            \n ● Choose the data to display using filters\
            \n ● Get interactive charts\
            \n ● View and download (custom) data tables\
            \n ● Regulate access through a user interface\
            \n ● Access on both PC and smartphone\
            \n\n ► In the example that I am providing, I am working with a random database (Excel),\
                but this is possible with any type of database\
            \n ► In order to access the app please click on [Example APP] on the left side menu")
    
    with colpi2:
        st.markdown("<br>", unsafe_allow_html=True)
        lottie_dashb = load_lottiefile(lottie_dashb)
        st_lottie(
            lottie_dashb,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # medium ; high ; low
            height=250)
        
    st.markdown("<br>", unsafe_allow_html=True)
    esp_1, col_vid_tuto, esp_2 = st.columns([space, tuto_space, space], gap="small")
    with col_vid_tuto :
        with open(tuto_analyticdash, "rb") as tuto_file:
            tuto_analyticdash_byte = tuto_file.read()
        st.video(tuto_analyticdash_byte)

if nav_menu == 'Example APP':
    
    infos = st.info("Trial credentials : ID = invite | Password = invite")

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        # Original DF
        main_df = get_data_from_dataset(Excel_BdD)
        infos.empty()
    
        options_dash = st.sidebar.radio(label="Sections :", options=['Overview', 'View/Extract Data'],
            index=0,  label_visibility="hidden")

        if options_dash == 'Overview':
            col0F_f, col1F_f, col2F_f = st.columns(3)

            with col0F_f:           
                options_city = ["ALL"] + list(main_df["City"].unique())
                ville = st.multiselect(label="📌 City :",
                    options=options_city,
                    default="ALL", label_visibility="visible") # "hidden"
                if "ALL" in ville:
                    df_filtr  = main_df
                else:
                    df_filtr = main_df[main_df["City"].isin(ville)]
    
            with col1F_f:
                options_sex = ["ALL"] + list(df_filtr["Gender"].unique())
                sex = st.multiselect(label="📌 Gender :",
                    options=options_sex,
                    default="ALL", label_visibility="visible") # "hidden"
                if "ALL" in sex:
                    df_filtr  = df_filtr
                else:
                    df_filtr = df_filtr[df_filtr["Gender"].isin(sex)]

            with col2F_f:
                options_P = ["ALL"] + list(sorted(df_filtr["Type_produit"].unique()))
                type_p = st.multiselect(label="📌 Product type :",
                    options=options_P,
                    default="ALL", label_visibility="visible") # "hidden"
                if "ALL" in type_p:
                    df_filtr  = df_filtr
                else:
                    df_filtr = df_filtr[df_filtr["Type_produit"].isin(type_p)]

            st.markdown("""---""")
        
            # Main KPI's
            tot_Achats = round(total_kpi(df_filtr)[0], 1)
            tot_ventes = round(total_kpi(df_filtr)[1], 1)
            tot_taxes = round(total_kpi(df_filtr)[2], 1)
            tot_profit_net = round(total_kpi(df_filtr)[3], 1)

            col0, col1, col2, col3 = st.columns(4)
            with col0:
                st.subheader("Total Purchases")
                st.subheader(f"{tot_Achats:,} $".format(tot_Achats).replace(',', ' '))
                # st.subheader(f"T {total_Arr:,}")
            with col1:
                st.subheader("Total Sales")
                st.subheader(f"{tot_ventes:,} $".format(tot_ventes).replace(',', ' '))
            with col2:
                st.subheader("Total Taxes")
                st.subheader(f"{tot_taxes:,} $".format(tot_taxes).replace(',', ' '))
            with col3:
                st.subheader("Net Profit")
                st.subheader(f"{tot_profit_net:,} $".format(tot_profit_net).replace(',', ' '))

            st.markdown("""---""")

            col_1_0, col_1_1 = st.columns(2)
            with col_1_0:
                st.subheader("Sales by Gender")
                st.plotly_chart(piechart_sales_gender(df_filtr), use_container_width=True) 

            with col_1_1:
                st.subheader("Sales by city")
                st.plotly_chart(piechart_sales_city(df_filtr), use_container_width=True)

            st.markdown("""---""")

            st.subheader("Sales volume by payment method")
            st.plotly_chart(bar_chart_pay_type(df_filtr), use_container_width=True)

            st.markdown("""---""")

            st.subheader("Evolution by week")
            st.plotly_chart(get_data_sem_chart(df_filtr), use_container_width=True)


        if options_dash == 'View/Extract Data':

            col0Fa_f, col1Fa_f, col2Fa_f = st.columns(3)

            with col0Fa_f:           
                options_city_a = ["ALL"] + list(main_df["City"].unique())
                ville_a = st.multiselect(label="📌 City :",
                    options=options_city_a,
                    default="ALL", label_visibility="visible") # "hidden"
                if "ALL" in ville_a:
                    df_filtr_a  = main_df
                else:
                    df_filtr_a = main_df[main_df["City"].isin(ville_a)]
    
            with col1Fa_f:
                options_sex_a = ["ALL"] + list(df_filtr_a["Gender"].unique())
                sex_a = st.multiselect(label="📌 Gender :",
                    options=options_sex_a,
                    default="ALL", label_visibility="visible") # "hidden"
                if "ALL" in sex_a:
                    df_filtr_a  = df_filtr_a
                else:
                    df_filtr_a = df_filtr_a[df_filtr_a["Gender"].isin(sex_a)]

            with col2Fa_f:
                options_P_a = ["ALL"] + list(sorted(df_filtr_a["Type_produit"].unique()))
                type_p_a = st.multiselect(label="📌 Product type :",
                    options=options_P_a,
                    default="ALL", label_visibility="visible") # "hidden"
                if "ALL" in type_p_a:
                    df_filtr_a  = df_filtr_a
                else:
                    df_filtr_a = df_filtr_a[df_filtr_a["Type_produit"].isin(type_p_a)]

            st.markdown("""---""")

            data_extract_df = get_showndf(df_filtr_a)
            
            temp = tempfile.NamedTemporaryFile(delete=True)
            temp_filename = temp.name + f'.xlsx'
            data_extract_df.to_excel(temp_filename, sheet_name='Data', index=False)

            last_file = curstom_excel_df(temp_filename)

            with open(last_file, "rb") as f:
                binary_data = f.read()

            timestr = time.strftime("%d-%H%M%S")
            excel_namefile  = f"Data_{timestr}.xlsx"

            st.download_button(
                label="Download Data to Excel",
                data=binary_data,
                file_name=excel_namefile)
            st.dataframe(data_extract_df.style.format(na_rep='No Data', precision=1), use_container_width=True)


        # Auth Logout
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
        st.sidebar.divider()
        authenticator.logout("Log Out", "sidebar")
