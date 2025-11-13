import streamlit as st
import pandas as pd
from io import BytesIO
from lary_agent import criar_agent
from dotenv import load_dotenv
import json
load_dotenv()

st.set_page_config(page_title="Analisador de Gênero", page_icon="👤", layout="centered")

st.title("👤 Analisador de Gênero por Username")

# Escolha do modelo
modelo_escolhido = st.selectbox(
    "Modelo de IA",
    [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "meta-llama/llama-guard-4-12b"
    ]
)

# Escolha da plataforma
plataforma = st.selectbox("Escolha a plataforma:", ["Instagram", "TikTok"])

# Input dos usernames
usernames_input = st.text_area(
    "Lista nomes de perfis",
    placeholder="Ex: kipper.dev, lucasluc25, ramon.pelle"
)

st.write("Insira uma lista de nomes de perfis separados por vírgula para analisar")

# Pré-processamento e contagem
if usernames_input.strip():
    # Separar por vírgula e remover espaços
    raw_list = [u.strip() for u in usernames_input.split(",") if u.strip()]
    # Remover múltiplos espaços internos
    clean_list = [' '.join(u.split()) for u in raw_list]
    # Remover duplicados mantendo ordem
    unique_list = []
    for u in clean_list:
        if u not in unique_list:
            unique_list.append(u)
    total = len(raw_list)
    total_unicos = len(unique_list)
    repetidos = total - total_unicos
    st.markdown(
        f"**📋 Lista total:** {total}  "
        f"**🔁 Repetidos:** {repetidos}  "
        f"**✅ Lista total SEM repetidos:** {total_unicos}"
    )

# Processar usernames
if st.button("Analisar"):
    if not usernames_input.strip():
        st.warning("Por favor, insira ao menos um username.")
    else:
        # 1️⃣ Separar por vírgula e limpar nomes
        raw_list = [u.strip() for u in usernames_input.split(",") if u.strip()]
        clean_list = [' '.join(u.split()) for u in raw_list]

        # 2️⃣ Remover duplicados mantendo a ordem
        list_username = []
        for u in clean_list:
            if u not in list_username:
                list_username.append(u)

        # Criar dicionário username → link
        if plataforma == "Instagram":
            usernames_dict = {u: f"https://www.instagram.com/{u}/" for u in list_username}
        else:
            usernames_dict = {u: f"https://www.tiktok.com/@{u}" for u in list_username}

        agent = criar_agent(modelo_escolhido)

        # Chamar a IA para identificar apenas o sexo
        response = agent.run(
            input=f"Identifique apenas o sexo (homem, mulher, indeterminado) "
                  f"para os seguintes usernames: {list(usernames_dict.keys())}"
        )

        sexos = json.loads(response.content)

        # Montar DataFrame completo
        data = [
            {"username": u, "link": link, "sexo": sexos.get(u, "indeterminado")}
            for u, link in usernames_dict.items()
        ]
        df = pd.DataFrame(data)

        # ✅ Ordenar pelo sexo: mulheres → homens → indeterminado
        sexo_order = pd.CategoricalDtype(categories=["mulher", "homem", "indeterminado"], ordered=True)
        df["sexo"] = df["sexo"].astype(sexo_order)
        # Opcional: ordenar também pelo username dentro de cada sexo
        df = df.sort_values(["sexo", "username"]).reset_index(drop=True)

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
