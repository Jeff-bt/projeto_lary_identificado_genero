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

plataforma = st.selectbox("Escolha a plataforma:", ["Instagram", "TikTok"])

# Input dos usernames
usernames_input = st.text_area("Usernames", placeholder="Ex: kipper.dev, lucasluc25, ramon.pelle")

if usernames_input.strip():
    # Quebra por vírgula e remove espaços extras
    raw_list = [u.strip() for u in usernames_input.split(",") if u.strip()]

    # Remove duplicados mantendo a ordem
    unique_list = []
    for u in raw_list:
        if u not in unique_list:
            unique_list.append(u)

    # Calcula os totais
    total = len(raw_list)
    total_unicos = len(unique_list)
    repetidos = total - total_unicos

    # Mostra os resultados
    st.markdown(f"**📋 Total digitado:** {total}  **🔁 Repetidos:** {repetidos}  **✅ Sem repetidos:** {total_unicos}")

# Processar usernames
if st.button("Analisar"):
    if usernames_input.strip() == "":
        st.warning("Por favor, insira ao menos um username.")
    else:
        list_username = list(set([u.strip() for u in usernames_input.split(",") if u.strip()]))

        if plataforma == "Instagram":
            usernames_dict = {u: f"https://www.instagram.com/{u}/" for u in list_username}
        else:  # TikTok
            usernames_dict = {u: f"https://www.tiktok.com/@{u}" for u in list_username}

        print(usernames_dict)

        response = agent.run(input=str(f"é: {plataforma} {list_username}"))

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
