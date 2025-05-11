import streamlit as st
import pandas as pd
import os
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Baixa stopwords uma vez
nltk.download('stopwords')

def gerar_nuvem_palavras_df(df, complemento=''):
    all_words = []

    emoji_pattern = r':[a-zA-Z0-9-_]+:'  # padrão de emoji tipo :smile:

    for msg in df['message'].dropna().astype(str):
        msg = msg.lower()
        msg = re.sub(emoji_pattern, '', msg)  # remove emojis estilo Discord
        msg = re.sub(r'[^\w\s]', '', msg)  # remove pontuação
        words = msg.split()
        all_words.extend(words)

    text = ' '.join(all_words)
    stop_words = set(stopwords.words('portuguese'))
    stop_words.update(["https", "http", "rt", "pra", "tá", "né", "vai"])  # extras

    wordcloud = WordCloud(
        stopwords=stop_words,
        background_color='white',
        width=1920,
        height=1080
    ).generate(text)

    # Salva localmente
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'nuvem_palavras{complemento}.png')
    wordcloud.to_file(output_file)

    return output_file