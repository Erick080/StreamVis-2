import streamlit as st
import pandas as pd
from detoxify import Detoxify
from tqdm import tqdm
tqdm.pandas()

@st.cache_resource
def carregar_modelo():
    with st.spinner("Downloading Detoxify model... this can take a few seconds the first time."):
        return Detoxify("multilingual", device="cpu")

@st.cache_data
def classificar(texto, _modelo):
    predicoes = _modelo.predict(texto)
    return {rotulo: float(valor) for rotulo, valor in predicoes.items()}

def detoxify_page():
    st.title("Toxicity Detection with Detoxify")
    
    if "analyzed_csv_files" not in st.session_state or not st.session_state.analyzed_csv_files:
        st.warning('No data uploaded, please upload some data before checking this page')
        return

    file_name = st.selectbox('Uploaded archives', st.session_state.analyzed_csv_files.keys())
    dfComentarios = st.session_state.analyzed_csv_files[file_name]

    modelo = carregar_modelo() 
    if st.button("Run Detoxify"):
        with st.spinner("Analysing toxicity..."):
            seriePredicoes = dfComentarios["message"].progress_apply(lambda msg: classificar(msg, modelo))
            # Converte para DataFrame e concatena aos comentários originais
            dfPredicoes = pd.json_normalize(seriePredicoes)
            dfFinal = pd.concat([dfComentarios, dfPredicoes], axis=1)
            st.session_state.analyzed_csv_files[file_name] = dfFinal
            st.success("Analysis finished!")

        json_resultado = dfFinal.to_json(orient="records", force_ascii=False, indent=2)
        
        st.download_button(
            label="Download result as JSON",
            data=json_resultado,
            file_name="resultado_toxicidade.json",
            mime="application/json"
        )

