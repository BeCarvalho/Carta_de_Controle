import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# Função para calcular limites da carta de controle
def calcular_limites(dados):
    media = dados['Valor'].mean()
    desvio_padrao = dados['Valor'].std()
    limite_superior = media + 3 * desvio_padrao
    limite_inferior = media - 3 * desvio_padrao
    return media, limite_superior, limite_inferior


# Função para gerar e salvar o gráfico em PDF
def salvar_pdf(nome_analise, dados, media, limite_superior, limite_inferior):
    # Criar um PDF com o gráfico e a tabela
    with PdfPages(f'{nome_analise}.pdf') as pdf:
        plt.figure(figsize=(10, 6))
        plt.plot(dados['Data'], dados['Valor'], marker='o', linestyle='-', color='blue', label='Valores')
        plt.axhline(y=media, color='green', linestyle='--', label='Média')
        plt.axhline(y=limite_superior, color='red', linestyle='--', label='LSC (Limite Superior)')
        plt.axhline(y=limite_inferior, color='orange', linestyle='--', label='LIC (Limite Inferior)')
        plt.xticks(rotation=45)
        plt.xlabel("Data Coleta")
        plt.ylabel("Valor")
        plt.title(f"Carta de Controle - {nome_analise}")
        plt.legend()
        plt.tight_layout()

        # Adicionar gráfico ao PDF
        pdf.savefig()
        plt.close()

        # Adicionar tabela ao PDF
        fig, ax = plt.subplots(figsize=(10, 4))  # Tamanho da tabela
        ax.axis('tight')
        ax.axis('off')
        table_data = dados[['Data', 'Valor']].values
        table = ax.table(cellText=table_data, colLabels=['Data', 'Valor'], cellLoc='center', loc='center')

        # Adicionar tabela ao PDF
        pdf.savefig()
        plt.close()


# Interface do Streamlit
st.title("Análise de Controle Laboratorial")

# Seleção do tipo de análise
tipo_analise = st.selectbox("Selecione o tipo de análise:", ["Colimetria (Quantitativa)", "Esporos de Bactérias Aeróbias - EBA"])

# Upload dos dados
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Carregar os dados e exibir as colunas
    try:
        dados = pd.read_csv(uploaded_file, delimiter=",", decimal=",")

        # Certifique-se de que as colunas estão no formato correto
        dados['Data'] = pd.to_datetime(dados['Data'], format="%d/%m/%Y")
        dados['Valor'] = pd.to_numeric(dados['Valor'], errors='coerce')

        # Exibir os dados carregados
        st.subheader("Dados Carregados")
        st.write(dados)

        # Calcular limites
        media, limite_superior, limite_inferior = calcular_limites(dados)

        # Exibir a média e os limites de controle
        st.subheader("Métricas da Carta de Controle")
        st.write(f"Média: {media:.2f}")
        st.write(f"Limite Superior de Controle (LSC): {limite_superior:.2f}")
        st.write(f"Limite Inferior de Controle (LIC): {limite_inferior:.2f}")

        # Plotar a carta de controle
        plt.figure(figsize=(10, 6))
        plt.plot(dados['Data'], dados['Valor'], marker='o', linestyle='-', color='blue', label='Valores')
        plt.axhline(y=media, color='green', linestyle='--', label='Média')
        plt.axhline(y=limite_superior, color='red', linestyle='--', label='LSC (Limite Superior)')
        plt.axhline(y=limite_inferior, color='orange', linestyle='--', label='LIC (Limite Inferior)')
        plt.xticks(rotation=45)
        plt.xlabel("Data Coleta")
        plt.ylabel("Valor")
        plt.title(f"Carta de Controle - {tipo_analise}")
        plt.legend()

        st.pyplot(plt)

        # Botão para download do PDF
        if st.button("Baixar PDF com Gráfico e Tabela"):
            salvar_pdf(tipo_analise, dados, media, limite_superior, limite_inferior)
            st.success(f"PDF '{tipo_analise}.pdf' gerado com sucesso!")

    except KeyError as e:
        st.error(
            f"Erro: Coluna {e} não encontrada. Verifique se o arquivo CSV contém as colunas corretas ('Data' e 'Valor').")