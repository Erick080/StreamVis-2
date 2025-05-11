import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def categories_page():
    st.title('Category charts based on the uploaded analzyed data')

    if "analyzed_csv_files" not in st.session_state or not st.session_state.analyzed_csv_files:
        st.warning('No data uploaded, please upload some data before checking this page')
        return
    
    combined_counts = []

    classification_col = 'sentimento'

    for file_name, data in st.session_state.analyzed_csv_files.items():
        counts = data[classification_col].value_counts().reset_index()
        counts.columns = ['Classification', 'Count']
        counts['File Name'] = file_name
        combined_counts.append(counts)
        

    combined_data = pd.concat(combined_counts, ignore_index=True)

    classification_colors = {
        "NEGATIVE": "red",
        "POSITIVE": "green",
        "NEUTRAL": "yellow",
    }   

    fig = go.Figure()

    for classification in combined_data["Classification"].unique():
        filtered_data = combined_data[combined_data["Classification"] == classification]
        fig.add_trace(go.Bar(
            name=classification,
            x=filtered_data["File Name"],
            y=filtered_data["Count"],
            marker_color = classification_colors.get(classification, "gray")
        ))

    # Configurar o layout do gráfico
    fig.update_layout(
        barmode="stack",
        title="Stacked Bar Chart of Classifications",
        xaxis_title="Source (Files)",
        yaxis_title="Count",
        legend_title="Classifications",
    )

    st.plotly_chart(fig)

    
