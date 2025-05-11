import streamlit as st
import pandas as pd

def analyzed_upload():
    DEFAULT_PATHS = {
        "Monark": "input/comentarios_Monark_Sentimentos.json"
    } 

    if "analyzed_csv_files" not in st.session_state:
        st.session_state.analyzed_csv_files = {}

    st.title('Csv Files Handler')

    if st.button('Upload default'):
        for name, path in DEFAULT_PATHS.items():
            try:
                df = pd.read_json(path)
                st.session_state.analyzed_csv_files[name] = df
            except Exception as e:
                print(e)

    #Upload
    analyzed_files = st.file_uploader('Dump analyzed csv files here', type=['csv', 'json'], accept_multiple_files =True)
    if analyzed_files:
        for file in analyzed_files:
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file, delimiter=';')
                elif file.name.endswith('.json'):
                    df = pd.read_json(file)
                else:
                    continue
                
                st.session_state.analyzed_csv_files[file.name] = df
                
            except Exception as e:
                st.error(f"Erro ao carregar {file.name}: {e}")
            
        
    
    #List and handle changes for uploaded archieves
    if st.session_state.analyzed_csv_files:
        file_name = st.selectbox('Uploaded archieves', st.session_state.analyzed_csv_files.keys())
        st.dataframe(st.session_state.analyzed_csv_files[file_name])

        if(st.button('Remove file')):
            del st.session_state.analyzed_csv_files[file_name]
    
    else:
        st.info('No csv archieve')