import streamlit as st
import pandas as pd
import zipfile
import io

st.set_page_config(page_title="NIW SmartBilling", layout="wide")

st.title("NIW SmartBilling")
st.write("Automatização do registo contabilístico das faturas NIW.")

uploaded_file = st.file_uploader("Carrega aqui o ficheiro ZIP com os dados NIW", type="zip")

if uploaded_file is not None:
    st.success("Ficheiro carregado com sucesso!")

    with zipfile.ZipFile(uploaded_file) as z:
        file_list = z.namelist()

        st.subheader("Ficheiros encontrados")
        st.write(file_list)

        dfs = {}

        for file in file_list:
            if file.endswith(".xlsx"):
                with z.open(file) as f:
                    dfs[file] = pd.read_excel(f)

        st.subheader("Pré-visualização dos ficheiros")

        for nome, df in dfs.items():
            st.write(f"### {nome}")
            st.write(df.head())
            st.write("Colunas:", list(df.columns))

        st.subheader("Resultado contabilístico automático")

        if len(dfs) > 0:
            primeiro_ficheiro = list(dfs.keys())[0]
            resultado = dfs[primeiro_ficheiro].copy()

            st.write(resultado)

            output = io.BytesIO()
            resultado.to_excel(output, index=False, engine="openpyxl")

            st.download_button(
                label="Download do ficheiro contabilístico",
                data=output.getvalue(),
                file_name="output_contabilistico.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
