import base64
import json
from io import BytesIO
import os  # <--- Biblioteca que o Python usa para ler as chaves do sistema
from openai import OpenAI  # <--- Biblioteca oficial da OpenAI
from PIL import Image
import streamlit as st

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(
    page_title="Nutri Fit AI | Performance & Dieta",
    page_icon="🏋️‍♂️",
    layout="centered",
)

# --- CSS PERSONALIZADO (FUNDO DE ACADEMIA) ---
url_fundo_academia = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1920&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url("{url_fundo_academia}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    h1, h2, h3 {{
        color: #39FF14 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}
    div.stTabs [data-baseweb="tab-panel"] {{
        background-color: rgba(20, 20, 20, 0.85);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #333;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.7);
    }}
    .stButton>button {{
        background-color: #39FF14 !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        box-shadow: 0px 0px 10px rgba(57, 255, 20, 0.4);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- CONFIGURAÇÃO DA CHAVE DA OPENAI ---
# O Python vai ler a chave automaticamente da variável de ambiente chamada OPENAI_API_KEY
# Se a chave não estiver configurada, ele avisa na tela para você configurar.
try:
  api_key = os.environ.get("OPENAI_API_KEY")
  if not api_key:
    st.error(
        "⚠️ ATENÇÃO: A chave da OpenAI (OPENAI_API_KEY) não foi encontrada no"
        " sistema. Configure a chave no seu terminal antes de rodar."
    )
    client = None
  else:
    # Cria o cliente oficial da OpenAI usando a sua chave de backend
    client = OpenAI(api_key=api_key)
except Exception as e:
  st.error(f"Erro ao inicializar o cliente OpenAI: {e}")
  client = None


# Função para converter imagem para base64
def imagem_para_base64(imagem):
  buffered = BytesIO()
  imagem.save(buffered, format="JPEG")
  return base64.b64encode(buffered.getvalue()).decode("utf-8")


# --- LAYOUT PRINCIPAL ---
st.markdown(
    "<h1 style='text-align: center;'>🏋️‍♂️ Nutri Fit AI</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='text-align: center; color: #FAFAFA !important;'>O seu personal"
    " nutricionista com IA na nuvem.</h3>",
    unsafe_allow_html=True,
)

# Abas na tela
aba1, aba2 = st.tabs(["📊 Definir Metas", "📸 Scannear Prato"])

with aba1:
  st.header("📊 Defina suas Metas e Perfil")
  st.write("Preencha seus dados para calcularmos seu TDEE e macros ideais.")

  col1, col2 = st.columns(2)
  with col1:
    peso = st.number_input("Peso (kg)", value=80.0, step=0.5)
    altura = st.number_input("Altura (cm)", value=175.0, step=1.0)
    idade = st.number_input("Idade", value=41, step=1)

  with col2:
    genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    nivel_atividade = st.selectbox(
        "Nível de Atividade Física",
        [
            "Sedentário (pouco ou nenhum exercício) 🛋️",
            "Levemente ativo (exercício leve 1-3 dias/sem) 🚶",
            "Moderadamente ativo (exercício moderado 3-5 dias/sem) 🏃‍♂️",
            "Muito ativo (exercício pesado 6-7 dias/sem) 🏋️‍♀️",
        ],
        index=2,
    )
    objetivo = st.selectbox(
        "Seu Objetivo",
        [
            "Ganhar massa e perder gordura (Recomposição) 🚀",
            "Perder peso e preservar a massa (Cutting) 🔥",
            "Emagrecer (Geral) 🍃",
        ],
    )

  if st.button("🚀 Calcular Minha Meta Fit"):
    if genero == "Masculino":
      tmb = (10 * peso) + (6.25 * altura) - (5 * idade) + 5
    else:
      tmb = (10 * peso) + (6.25 * altura) - (5 * idade) - 161

    fatores = {
        "Sedentário (pouco ou nenhum exercício) 🛋️": 1.2,
        "Levemente ativo (exercício leve 1-3 dias/sem) 🚶": 1.375,
        "Moderadamente ativo (exercício moderado 3-5 dias/sem) 🏃‍♂️": 1.55,
        "Muito ativo (exercício pesado 6-7 dias/sem) 🏋️‍♀️": 1.725,
    }
    tdee = tmb * fatores[nivel_atividade]

    if objetivo == "Ganhar massa e perder gordura (Recomposição) 🚀":
      calorias_meta = tdee
      proteina_por_kg = 2.4
    elif objetivo == "Perder peso e preservar a massa (Cutting) 🔥":
      calorias_meta = tdee - 400
      proteina_por_kg = 2.4
    else:
      calorias_meta = tdee - 500
      proteina_por_kg = 2.0

    meta_proteina = peso * proteina_por_kg

    st.success("✅ Metas Calculadas com Sucesso!")
    m1, m2, m3 = st.columns(3)
    m1.metric("🔥 Gasto Basal (TMB)", f"{int(tmb)} kcal")
    m2.metric("🎯 Meta Diária", f"{int(calorias_meta)} kcal")
    m3.metric("🍗 Meta de Proteína", f"{int(meta_proteina)}g")

with aba2:
  st.header("📸 Scannear Prato com IA")
  st.write("Tire uma foto ou suba a imagem do seu rango para análise rápida.")

  arquivo_foto = st.file_uploader(
      "Escolha a foto do prato...", type=["jpg", "jpeg", "png"]
  )

  if arquivo_foto is not None:
    imagem = Image.open(arquivo_foto)
    st.image(
        imagem,
        caption="Prato enviado para análise",
        use_column_width=True,
        output_format="JPEG",
    )

    if st.button("🔍 Analisar Refeição"):
      if not client:
        st.error(
            "❌ O cliente da OpenAI não está configurado. Verifique a chave da"
            " API."
        )
      else:
        with st.spinner(
            "🧠 Processando imagem na API oficial da OpenAI (GPT-4o-mini)..."
        ):
          try:
            base64_img = imagem_para_base64(imagem)

            prompt_sistema = (
                "Você é um nutricionista especialista em performance"
                " esportiva. Analise a imagem deste prato de comida."
                " Identifique os alimentos visíveis, estime o peso aproximado"
                " de cada item e retorne estritamente um JSON com o seguinte"
                ' formato (sem markdown ou crases, apenas o JSON puro):'
                ' {"alimentos": [{"nome": "...", "peso_g": ...}], '
                '"total_calorias": ..., "total_proteinas_g": ...}'
            )

            # Chamada direta para o modelo inteligente da OpenAI na nuvem
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_sistema},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_img}"
                            },
                        },
                    ],
                }],
                max_tokens=600,
            )

            texto_resposta = resposta.choices[0].message.content
            texto_limpo = (
                texto_resposta.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            st.subheader("📋 Resultado da Análise:")
            dados_json = json.loads(texto_limpo)

            cal_ref = dados_json.get("total_calorias", 0)
            prot_ref = dados_json.get("total_proteinas_g", 0)

            r1, r2 = st.columns(2)
            r1.metric("🍽️ Calorias Estimadas", f"{cal_ref} kcal")
            r2.metric("💪 Proteínas Estimadas", f"{prot_ref}g")

            st.write("**Itens Detectados:**")
            for alimento in dados_json.get("alimentos", []):
              st.markdown(f"- **{alimento['nome']}**: ~{alimento['peso_g']}g")

            with st.expander("Ver JSON Bruto"):
              st.json(dados_json)

          except Exception as e:
            st.error(f"❌ Erro ao processar a imagem na API: {e}")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #aaa;'>Desenvolvido por Papai Tech"
    " Inc.</p>",
    unsafe_allow_html=True,
)