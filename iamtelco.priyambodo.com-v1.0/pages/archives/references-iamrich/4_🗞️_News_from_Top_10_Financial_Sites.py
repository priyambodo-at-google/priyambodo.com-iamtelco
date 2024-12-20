import streamlit as st
import webbrowser
import os

st.set_page_config(page_icon="image/usd.ico")

vNoLabel = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(vNoLabel, unsafe_allow_html=True)

html_code = """
  <html>
    <head>
      <title>Discover Financial Articles</title>
      <style>
        .column {
            float: left;
            width: 50%;
        }
      </style>
    </head> 
  <body>
    <h1>Search quality articles from these Top 10 Best Financial News portal</h1>
    <p>
    In the realm of finance, staying informed is crucial. To help you access high-quality articles, we present a curated list of the top 10 financial news portals. These sources have established themselves as reliable outlets and insightful content. Stay informed, make informed decisions, and explore the world of finance through these reputable sources.
    </p>
    <p>
    Source of the articles:
    <br>
      <div class="column">
          <ul>
              <li>Forbes</li>
              <li>Bloomberg</li>
              <li>Reuters</li>
              <li>CNNMoney</li>
              <li>Wall Street Journal</li>
          </ul>
      </div>
      <div class="column">
          <ul>
              <li>TheStreet</li>
              <li>Financial Times</li>
              <li>MarketWatch</li>
              <li>Kiplinger</li>
              <li>This is Money</li>
          </ul>
      </div>
      </p>
      <p>
      Please search into the top 10 financial news portals from the box below: (ex: Google)
      </p>
    </body>
  </html>
"""
st.markdown(html_code, unsafe_allow_html=True)

def create_hyperlink_button(url, text):
  button_html = f'<a href="{url}" target="_blank">{text}</a>'
  return st.markdown(button_html, unsafe_allow_html=True)
url = "https://enterprisesearch-app-rzmyhdhywa-uc.a.run.app/news.html"
text = "Search your financial articles in here..."
create_hyperlink_button(url, text)