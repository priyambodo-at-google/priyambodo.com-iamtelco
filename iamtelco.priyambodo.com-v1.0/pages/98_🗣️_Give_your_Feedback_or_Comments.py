import streamlit as st
import streamlit.components.v1 as components

st.header('🗣️ Please :orange[give] :red[your] :green[feedback] or :blue[comments]', divider="rainbow")
st.write("Your feedback is very important for us to improve the quality of this application. Suggest new features or report bugs. Word of appreciation is also welcome.")

target_url = "https://docs.google.com/forms/d/e/1FAIpQLSewiNk6NjyX5KRN3B9EUKVeHgK6IIDcKwT0qqibzh6fCPYi8g/viewform?usp=published_options"
iframe_width = 800
iframe_height = 1800

components.iframe(target_url, width=iframe_width, height=iframe_height, scrolling=True)