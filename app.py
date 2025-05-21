from app_pages import landing_page
from app_pages.analyzed_comments.wordcloud import wordcloud_page
from app_pages.analyzed_comments.categories import categories_page
from app_pages.analyzed_comments.analyzed_upload import analyzed_upload
from app_pages.analyzed_comments.detoxify_analysis import detoxify_page
import streamlit as st

st.set_page_config(
    page_title='Views',
    page_icon='📊',
    layout='wide',
    menu_items={'Get Help': None, 'Report a Bug': None, 'About': None}
)

sub_section = ''


sub_section = st.sidebar.selectbox('Sub Section', ['Upload File', 'Categories', 'Wordcloud', 'Detoxify Analysis'])
match sub_section:
    case 'Upload File':
        analyzed_upload()
    case 'Categories':
        categories_page()
    case 'Wordcloud':
        wordcloud_page()
    case 'Detoxify Analysis':
        detoxify_page()
    case _:
        landing_page()
