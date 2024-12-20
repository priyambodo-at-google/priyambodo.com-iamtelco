import streamlit as st

st.header('☕ Check :orange["I Am"] other :red[Gen AI] :green[Apps] by :blue[Google]', divider="rainbow")
st.write("By harnessing the power of generative AI across diverse industry sectors, businesses are unlocking a new era of innovation, tackling real-world challenges with unprecedented efficiency and creativity. This widespread adoption signifies a pivotal shift in the technological landscape, marking a transition from theoretical possibilities to tangible, value-driven applications within the Enterprise environment.")

st.subheader('_Choose your other "I Am" application from here...:point_down:_')
st.write("The following applications are trying to solve real-world problems by implementing generative AI in multiple vertical industries, which represents real customer's use cases.")

columns = st.columns(3)

with columns[0]:
    st.image("./static/iamgemini.jpg")
    st.markdown("<p style='text-align:center'><strong>Showcasing The Power of AI</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'><small><a href='https://iamgemini.priyambodo.com'>https://iamgemini.priyambodo.com</a></small></p>", unsafe_allow_html=True)

with columns[1]:
    st.image("./static/iamrich.png")
    st.markdown("<p style='text-align:center'><strong>Financial Industry Advisor</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'><small><a href='https://iamrich.priyambodo.com'>https://iamrich.priyambodo.com</a></small></p>", unsafe_allow_html=True)

with columns[2]:
    st.image("./static/iamtelco.png")
    st.markdown("<p style='text-align:center'><strong>Telco Industry Advisor</strong></p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'><small><a href='https://iamtelco.priyambodo.com'>https://iamtelco.priyambodo.com</a></small></p>", unsafe_allow_html=True)