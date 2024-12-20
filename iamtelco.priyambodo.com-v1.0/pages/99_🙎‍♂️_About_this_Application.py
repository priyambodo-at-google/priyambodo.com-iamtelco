import streamlit as st
st.set_page_config(page_icon="image/usd.ico")
vNoLabel = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
html_code = """
    Boost your efficiency and unlock new possibilities with IamTelco, the cutting-edge Telco AI advisor. Leveraging the power of Google Cloud Generative AI and Gemini technology.
    """
with st.sidebar:
   st.success("Choose the menu that you would like to explore above 👆")
   st.info("app version: IamTelco v1.0-STABLE")
   st.image("static/doddihead.png", width=200)
   st.write("(c) Doddi Priyambodo")
   st.image("static/neelaksh.jpg", width=200)
   st.write("(c) Neelaksh Sharma")
   st.error("This application is created and maintained by Doddi Priyambodo & Neelaksh Sharma")

def run():
    st.markdown(vNoLabel, unsafe_allow_html=True)
    st.write("# About IamTelco")
    st.subheader("//powered by Google Cloud Generative AI!")
    st.write(html_code)
    st.write(
        """
        **This is the Technical Architecture** of IamTelco Application: 
        """
    )
    st.image("static/iamrich-arch.png")
    st.caption("the diagram is built with https://googlecloudcheatsheet.withgoogle.com/architecture")
    #st.sidebar.success("Select the use cases that you would like to see above.")

    st.markdown("---")    

if __name__ == "__main__":
    run()