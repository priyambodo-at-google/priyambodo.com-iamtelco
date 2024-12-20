import streamlit as st
from streamlit.logger import get_logger
#import authrich

#authrich.authenticate()
LOGGER = get_logger(__name__)

vNoLabel = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
html_code = """
    Boost your efficiency and unlock new possibilities with IamTelco, the cutting-edge Telco AI advisor. Leveraging the power of Google Cloud Generative AI and Gemini technology
    """

def run():
    st.set_page_config(page_icon="static/usd.ico")
    st.markdown(vNoLabel, unsafe_allow_html=True)
    st.header('🥷 :red[I am Telco]-v1 : Your ":blue[Gen AI] :green[Telco Advisor]"', divider="rainbow")
    st.caption("[https://iamrich.priyambodo.com] | [https://iamtelco.priyambodo.com] | [https://iamgemini.priyambodo.com]")
    st.subheader("//IamTelco is powered by Google Generative AI (Gemini)")
    st.write(html_code)
   
    st.markdown(
        """
        **👈 Select the menu from the sidebar** to start your experience. 
        """
    )
    st.image("static/logo.png", width=700)
    #st.sidebar.success("Select the use cases that you would like to see above.")
    st.write("(The logo image above is created by Google AI using Imagen 2 model.)")

    st.write("""
    <div style="text-align:center;padding:1em 0;"> 
        <table style="width: 100%;">
        <tr>
            <th style="color: gray; text-align: left;">Current local time in</th>
            <th style="text-align: left;">Jakarta, Indonesia</th>
        </tr>
        <tr>
            <td colspan="2">
            <iframe src="https://www.zeitverschiebung.net/clock-widget-iframe-v2?language=en&size=medium&timezone=Asia%2FJakarta" width="100%" height="115" frameborder="0" seamless></iframe>
            </td>
        </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        This application is maintained by <b>Doddi Priyambodo</b> (priyambodo@google.com | doddi@bicarait.com)   
        App Name & latest Version: <b>IamTelco-v1.0</b>
        """, unsafe_allow_html=True
    )
    
if __name__ == "__main__":
    run()
