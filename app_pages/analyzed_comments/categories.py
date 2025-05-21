import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def categories_page():
    st.title('Category charts based on the uploaded analyzed data')

    if "analyzed_csv_files" not in st.session_state or not st.session_state.analyzed_csv_files:
        st.warning('No data uploaded, please upload some data before checking this page')
        return

    # Verifica interseção de colunas entre todos os arquivos
    common_columns = set.intersection(*[set(df.columns) for df in st.session_state.analyzed_csv_files.values()])
    
    if not common_columns:
        st.error("No common columns found in uploaded files.")
        return

    # Permite o usuário escolher qual coluna usar como categoria
    selected_column = st.selectbox(
        "Select the category column to visualize:",
        sorted(common_columns),
        index=sorted(common_columns).index("sentimento") if "sentimento" in common_columns else 0
    )

    combined_counts = []

    for file_name, data in st.session_state.analyzed_csv_files.items():
        if selected_column not in data.columns:
            continue
        counts = data[selected_column].value_counts().reset_index()
        counts.columns = ['Classification', 'Count']
        counts['File Name'] = file_name
        combined_counts.append(counts)

    if not combined_counts:
        st.warning(f"No data found for selected column: {selected_column}")
        return

    combined_data = pd.concat(combined_counts, ignore_index=True)

    # Cores opcionais para sentimento. Pode-se expandir conforme outras categorias
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
            marker_color=classification_colors.get(classification, "gray")
        ))

    fig.update_layout(
        barmode="stack",
        title=f"Stacked Bar Chart of '{selected_column}' Classifications",
        xaxis_title="Source (Files)",
        yaxis_title="Count",
        legend_title="Classifications",
    )

    st.plotly_chart(fig)

