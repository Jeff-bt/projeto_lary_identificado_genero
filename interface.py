import streamlit as st
import pandas as pd
from io import BytesIO
from lary_agent import agent
from dotenv import load_dotenv
import json
load_dotenv()

st.set_page_config(page_title="Analisador de Gênero", page_icon="👤", layout="centered")

st.title("👤 Analisador de Gênero por Username")

st.write("Insira uma lista de usernames separados por vírgula para analisar:")

# Input dos usernames
usernames_input = st.text_area("Usernames", placeholder="Ex: kipper.dev, lucasluc25, ramon.pelle")

# Processar usernames
if st.button("Analisar"):
    if usernames_input.strip() == "":
        st.warning("Por favor, insira ao menos um username.")
    else:
        list_username = [u.strip() for u in usernames_input.split(",") if u.strip()]

        usernames_dict = {username: f"https://www.instagram.com/{username}/" for username in list_username}
        print(usernames_dict)

        response = agent.run(input=str(list_username))

        df = pd.DataFrame(json.loads(response.content))

        # Mostrar tabela
        st.subheader("📊 Resultados")
        st.dataframe(df, use_container_width=True)

        # Contagens
        total = len(df)
        total_homens = (df["sexo"] == "homem").sum()
        total_mulheres = (df["sexo"] == "mulher").sum()
        total_indeterminado = (df["sexo"] == "indeterminado").sum()

        st.markdown(f"""
        ### 🔢 Totais
        - **Total geral:** {total}
        - 👨 Homens: {total_homens} ({(total_homens / total) * 100:.2f}%)
        - 👩 Mulheres: {total_mulheres} ({(total_mulheres / total) * 100:.2f}%)
        - ❓ Indeterminados: {total_indeterminado} ({(total_indeterminado / total) * 100:.2f}%)
        """)

        # Download XLSX
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Resultados')

        st.download_button(
            label="📥 Baixar XLSX",
            data=buffer.getvalue(),
            file_name="resultado_genero.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
