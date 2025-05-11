import streamlit as st
from nuvem import gerar_nuvem_palavras_df

def wordcloud_page():
    st.title('Individual analysis page')

    if "analyzed_csv_files" not in st.session_state or not st.session_state.analyzed_csv_files:
        st.warning('No data uploaded, please upload some data before checking this page')
        return
    
    file_name = st.selectbox('Uploaded archieves', st.session_state.analyzed_csv_files.keys())

    classification_col = ['Desempate']

    if file_name:
        st.image(gerar_nuvem_palavras_df(st.session_state.analyzed_csv_files[file_name]), file_name)
        