import base64
import json
from io import BytesIO
from openai import OpenAI
from PIL import Image
import streamlit as st

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(
    page_title="Nutri Fit AI | Performance & Hardware",
    page_icon="🏋️‍♂️",
    layout="centered",
)

# --- CSS PERSONALIZADO (FUNDO DE ACADEMIA + TEMA FIT) ---
# Usamos uma imagem de alta qualidade de academia/pesos com um overlay escuro
url_fundo_academia = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1920&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
    /* Fundo geral da aplicação com imagem de academia e escurecimento */
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url("{url_fundo_academia}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Estilização dos títulos */
    h1, h2, h3 {{
        color: #39FF14 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}

    /* Caixa de destaque para os blocos (cards translúcidos) */
    div.stTabs [data-baseweb="tab-panel"] {{
        background-color: rgba(20, 20, 20, 0.85);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #333;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.7);
    }}

    /* Ajuste das abas */
    .stTabs button {{
        font-weight: bold;
        color: #FAFAFA !important;
    }}

    /* Estilo dos botões principais */
    .stButton>button {{
        background-color: #39FF14 !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        box-shadow: 0px 0px 10px rgba(57, 255, 20, 0.4);
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        background-color: #32cd32 !important;
        box-shadow: 0px 0px 15px rgba(57, 255, 20, 0.8);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- CONEXÃO COM IA LOCAL ---
try:
  client = OpenAI(base_url="http://192.168.18.195:1234/v1", api_key="lm-studio")
except Exception as e:
  st.error(f"Erro ao conectar com o cliente OpenAI: {e}")
  st.stop()


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
    "<h3 style='text-align: center; color: #FAFAFA !important;'>Força,"
    " Disciplina e Precisão na Dieta.</h3>",
    unsafe_allow_html=True,
)

# Abas na tela
aba1, aba2 = st.tabs(["📊 Definir Metas", "📸 Scannear Prato"])

with aba1:
  st.header("📊 Defina suas Metas e Perfil")
  st.write(
      "Preencha seus dados para calcularmos seu TDEE e macros de alta"
      " performance."
  )

  col1, col2 = st.columns(2)
  with col1:
    peso = st.number_input(
        "Peso (kg)", value=80.0, step=0.5, help="Seu peso corporal atual."
    )
    altura = st.number_input(
        "Altura (cm)", value=175.0, step=1.0, help="Sua altura em centímetros."
    )
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

    st.success("✅ Metas Calculadas com Sucesso! Bora pra cima!")

    m1, m2, m3 = st.columns(3)
    m1.metric("🔥 Gasto Basal (TMB)", f"{int(tmb)} kcal")
    m2.metric("🎯 Meta Diária", f"{int(calorias_meta)} kcal")
    m3.metric("🍗 Meta de Proteína", f"{int(meta_proteina)}g")

with aba2:
  st.header("📸 Scannear Prato com IA Local")
  st.write("Tire uma foto ou suba a imagem do seu rango para análise rápida.")

  modelo_local = st.text_input(
      "Nome do modelo carregado no LM Studio", value="qwen2-vl-7b-instruct"
  )
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
      with st.spinner("🧠 Processando imagem no seu hardware local..."):
        try:
          base64_img = imagem_para_base64(imagem)

          prompt_sistema = (
              "Você é um nutricionista especialista em performance esportiva. Analise a imagem deste"
              " prato de comida. Identifique os alimentos visíveis, estime o peso"
              " aproximado de cada item e retorne estritamente um JSON com o seguinte"
              ' formato (sem usar blocos de código markdown ou crases, apenas'
              ' o texto do JSON puro): {"alimentos": [{"nome": "...",'
              ' "peso_g": ...}], "total_calorias": ...,'
              ' "total_proteinas_g": ...}'
          )

          resposta = client.chat.completions.create(
              model=modelo_local,
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
          try:
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

          except json.JSONDecodeError:
            st.error(
                "❌ Erro ao ler os dados retornados pela IA. O modelo retornou"
                " formato inválido."
            )
            st.code(texto_limpo)

        except Exception as e:
          st.error(
              f"❌ Erro ao conectar com o servidor local. O LM Studio está com o"
              f" servidor ligado? Erro: {e}"
          )

# --- RODAPÉ ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #aaa; text-shadow: 1px 1px 2px"
    " rgba(0,0,0,0.9);'>Desenvolvido por Papai Tech Inc. | 100% Local</p>",
    unsafe_allow_html=True,
)