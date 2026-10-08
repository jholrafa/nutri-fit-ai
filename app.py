import os
import streamlit as st
from PIL import Image
from openai import OpenAI

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Nutri Fit AI - Seu Personal & Nutri na Nuvem",
    page_icon="🏋️‍♂️",
    layout="centered",
)

# --- ESTILIZAÇÃO CSS (TEMA HARDCORE / ACADEMIA) ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #00FF66 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        background-color: #00FF66;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00cc52;
        color: #ffffff;
    }
    .stInfo {
        background-color: rgba(20, 20, 20, 0.85);
        color: #ffffff;
        border-left: 5px solid #00FF66;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Inicialização do Cliente OpenAI (Lendo da nuvem ou do ambiente local)
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
  try:
    api_key = st.secrets.get("OPENAI_API_KEY")
  except Exception:
    pass

client = OpenAI(api_key=api_key) if api_key else None

# Título Principal do App
st.markdown(
    "<h1 style='text-align: center;'>⚡ Nutri Fit AI</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 style='text-align: center; color: #a0a0a0;'>O seu personal"
    " nutricionista com IA na nuvem.</h4>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Abas de Navegação do Aplicativo
aba_metas, aba_scanner, aba_exercicios = st.tabs(
    [
        "📊 Definir Metas & Dieta",
        "📸 Scannear Prato (IA)",
        "🏋️‍♂️ Guia de Exercícios & Anatomia 3D",
    ]
)

# ==========================================
# ABA 1: METAS & DIETA
# ==========================================
with aba_metas:
  st.markdown("### 🎛️ Defina suas Metas e Perfil")
  st.write(
      "Preencha seus dados para calcularmos seu TDEE, macros ideias e o foco"
      " estratégico."
  )

  col1, col2 = st.columns(2)
  with col1:
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=80.0)
    altura = st.number_input(
        "Altura (cm)", min_value=100.0, max_value=230.0, value=175.0
    )
    idade = st.number_input("Idade", min_value=10, max_value=100, value=41)

  with col2:
    genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
    nivel_atividade = st.selectbox(
        "Nível de Atividade Física",
        [
            "Sedentário (pouco ou nenhum exercício)",
            "Levemente ativo (exercício leve 1-3 dias/sem)",
            "Moderadamente ativo (exercício moderado 3-5 dias/sem)",
            "Altamente ativo (exercício pesado 6-7 dias/sem)",
        ],
    )
    objetivo = st.selectbox(
        "Seu Objetivo",
        [
            "Ganhar massa e perder gordura (Recomposição) 🚀",
            "Perder peso e preservar a massa (Cutting) 🔥",
            "Emagrecer (Geral) 🍃",
        ],
    )

  if "Recomposição" in objetivo:
    st.info(
        "💡 **Sobre este método:** Ideal para ganhar massa muscular e queimar"
        " gordura ao mesmo tempo, mantendo as calorias equilibradas e alta"
        " proteína."
    )
  elif "Cutting" in objetivo:
    st.info(
        "💡 **Sobre este método:** Focado em secar e perder peso rápido, com"
        " déficit calórico estratégico e alto consumo de proteínas para"
        " preservar a massa magra."
    )
  else:
    st.info(
        "💡 **Sobre este método:** Perfeito para emagrecimento geral e"
        " redução de medidas de forma saudável."
    )

  if st.button("🔥 Calcular Minha Meta Fit"):
    if genero == "Masculino":
      tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
      tmb = 10 * peso + 6.25 * altura - 5 * idade - 161

    if "Sedentário" in nivel_atividade:
      tdee = tmb * 1.2
    elif "Levemente" in nivel_atividade:
      tdee = tmb * 1.375
    elif "Moderadamente" in nivel_atividade:
      tdee = tmb * 1.55
    else:
      tdee = tmb * 1.725

    if "Recomposição" in objetivo:
      calorias_alvo = int(tdee)
    elif "Cutting" in objetivo:
      calorias_alvo = int(tdee - 400)
    else:
      calorias_alvo = int(tdee - 500)

    proteina_alvo = int(peso * 2.2)

    st.success("🎯 Metas Calculadas com Sucesso!")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Gasto Diário (TDEE)", f"{int(tdee)} kcal")
    col_m2.metric("Calorias Alvo", f"{calorias_alvo} kcal")
    col_m3.metric("Proteína Recomendada", f"{proteina_alvo} g/dia")

# ==========================================
# ABA 2: SCANNER DE PRATOS (IA COM VISÃO)
# ==========================================
with aba_scanner:
  st.markdown("### 📸 Scanner Inteligente de Refeições")
  st.write(
      "Envie a foto do seu prato para a IA analisar os macronutrientes em"
      " segundos."
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
    )

    if st.button("🔍 Analisar Prato com IA"):
      if not client:
        st.error(
            "Erro: Chave da OpenAI não configurada. Verifique os Secrets ou o"
            " ambiente."
        )
      else:
        with st.spinner("Analisando imagem com inteligência artificial..."):
          try:
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um nutricionista esportivo rigoroso e um"
                            " sistema de visão computacional de segurança."
                            " Verifique se a imagem contém comida. Se for"
                            " objeto inválido (tijolo, animal, selfie),"
                            " retorne 'ERRO_IMAGEM_INVALIDA'. Se for comida,"
                            " estime calorias e macros em Markdown."
                        ),
                    },
                    {"role": "user", "content": "Analise esta refeição."},
                ],
            )
            resultado_ia = resposta.choices[0].message.content

            if "ERRO_IMAGEM_INVALIDA" in resultado_ia:
              st.error(
                  "🚨 **Alerta:** A imagem não parece ser uma refeição válida."
                  " Envie uma foto clara do prato."
              )
            else:
              st.markdown("### 📋 Relatório Nutricional")
              st.markdown(resultado_ia)
          except Exception as e:
            st.error(f"Erro ao processar imagem: {e}")

# ==========================================
# ABA 3: GUIA DE EXERCÍCIOS & ANATOMIA 3D (LOCAL)
# ==========================================
with aba_exercicios:
  st.markdown("### 🏋️‍♂️ Guia Técnico Visual com Bonequinhos 3D")
  st.write(
      "Selecione o grupo e o exercício para ver a ilustração anatômica exata"
      " e o passo a passo para iniciantes."
  )

  grupo_muscular = st.selectbox(
      "Selecione o Grupo Muscular:",
      [
          "Peitoral (Supinos e Crucifixos) 🦾",
          "Costas / Dorsal (Puxadas e Remadas) 🦾",
          "Braços (Bíceps e Tríceps) 🦾",
          "Ombros (Deltoides) 🦾",
          "Membros Inferiores (Pernas) 🦿",
      ],
  )

  if "Peitoral" in grupo_muscular:
    ex_peito = st.selectbox(
        "Exercício:",
        [
            "Supino Reto com Barra",
            "Supino Inclinado com Halteres",
            "Crucifixo na Polia",
        ],
    )

    if "Supino Reto" in ex_peito:
      st.markdown("#### 💥 Supino Reto com Barra")
      if os.path.exists("assets/supino_reto.jpg"):
        st.image(
            "assets/supino_reto.jpg",
            caption="Anatomia 3D - Foco no Peitoral e Tríceps",
            use_column_width=True,
        )
      else:
        st.warning(
            "⚠️ Imagem 'supino_reto.jpg' não encontrada na pasta 'assets'."
        )
      st.info(
          "🎯 **Como fazer (Iniciante):** Deite no banco, mantenha os pés firmes"
          " no chão e as escápulas coladas para trás. Segure a barra na largura"
          " dos ombros, desça controlando até tocar levemente a linha do peito"
          " e empurre para cima.\n\n- **Dica de Ouro:** Não estique totalmente"
          " os cotovelos no topo para manter a tensão constante no peitoral."
      )

    elif "Inclinado" in ex_peito:
      st.markdown("#### 💥 Supino Inclinado com Halteres")
      if os.path.exists("assets/supino_inclinado.jpg"):
        st.image(
            "assets/supino_inclinado.jpg",
            caption="Anatomia 3D - Foco no Peitoral Superior",
            use_column_width=True,
        )
      else:
        st.warning(
            "⚠️ Imagem 'supino_inclinado.jpg' não encontrada na pasta 'assets'."
        )
      st.info(
          "🎯 **Como fazer (Iniciante):** Ajuste o banco em um ângulo de 30 a"
          " 45 graus. Segure os halteres ao lado do peito superior e empurre"
          " para cima controlando o movimento."
      )

    else:
      st.markdown("#### 💥 Crucifixo na Polia")
      if os.path.exists("assets/Crucifixo_na_Polia.jpg"):
        st.image(
            "assets/Crucifixo_na_Polia.jpg",
            caption="Anatomia 3D - Isolamento do Peitoral",
            use_column_width=True,
        )
      elif os.path.exists("assets/crucifixo.jpg"):
        st.image(
            "assets/crucifixo.jpg",
            caption="Anatomia 3D - Isolamento do Peitoral",
            use_column_width=True,
        )
      else:
        st.warning("⚠️ Imagem do crucifixo não encontrada na pasta 'assets'.")
      st.info(
          "🎯 **Como fazer (Iniciante):** Fique no meio dos cabos, com os"
          " braços levemente flexionados (como se estivesse abraçando uma"
          " árvore) e feche as mãos na altura do peito."
      )

  elif "Costas" in grupo_muscular:
    ex_costas = st.selectbox(
        "Exercício:", ["Puxada Alta na Polia", "Remada Curvada com Barra"]
    )
    if "Puxada" in ex_costas:
      st.markdown("#### 💥 Puxada Alta na Polia")
      if os.path.exists("assets/puxada_alta.jpg"):
        st.image(
            "assets/puxada_alta.jpg",
            caption="Anatomia 3D - Foco no Grande Dorsal",
            use_column_width=True,
        )
      else:
        st.warning(
            "⚠️ Imagem 'puxada_alta.jpg' não encontrada na pasta 'assets'."
        )
      st.info(
          "🎯 **Como fazer (Iniciante):** Sente na máquina com os joelhos"
          " travados. Puxe a barra em direção ao peito estufando o tronco e"
          " puxando com os cotovelos para baixo."
      )
    else:
      st.markdown("#### 💥 Remada Curvada com Barra")
      if os.path.exists("assets/remada_curvada.jpg"):
        st.image(
            "assets/remada_curvada.jpg",
            caption="Anatomia 3D - Foco na Espessura das Costas",
            use_column_width=True,
        )
      else:
        st.warning(
            "⚠️ Imagem 'remada_curvada.jpg' não encontrada na pasta 'assets'."
        )
      st.info(
          "🎯 **Como fazer (Iniciante):** Incline o tronco a 45 graus com a"
          " coluna reta e puxe a barra na direção do umbigo."
      )

  elif "Braços" in grupo_muscular:
    ex_braco = st.selectbox(
        "Exercício:", ["Rosca Direta com Barra W", "Tríceps na Polia (Corda)"]
    )
    if "Rosca" in ex_braco:
      st.markdown("#### 💥 Rosca Direta com Barra W")
      if os.path.exists("assets/rosca_direta.jpg"):
        st.image(
            "assets/rosca_direta.jpg",
            caption="Anatomia 3D - Foco no Bíceps",
            use_column_width=True,
        )
      else:
        st.warning(
            "⚠️ Imagem 'rosca_direta.jpg' não encontrada na pasta 'assets'."
        )
      st.info(
          "🎯 **Como fazer (Iniciante):** Fique em pé com os cotovelos colados"
          " nas costelas. Suba a barra controlando o peso e desça devagar."
      )
    else:
      st.markdown("#### 💥 Tríceps na Polia (Corda)")
      if os.path.exists("assets/triceps_polia.jpg"):
        st.image(
            "assets/triceps_polia.jpg",
            caption="Anatomia 3D - Foco no Tríceps",
            use_column_width=True,
        )
      else:
        st.warning(
            "⚠️ Imagem 'triceps_polia.jpg' não encontrada na pasta 'assets'."
        )
      st.info(
          "🎯 **Como fazer (Iniciante):** Segure a corda com os cotovelos fixos"
          " ao lado do corpo e empurre para baixo, abrindo as pontas da corda"
          " no final."
      )

  elif "Ombros" in grupo_muscular:
    st.selectbox("Exercício:", ["Desenvolvimento com Halteres"])
    st.markdown("#### 💥 Desenvolvimento com Halteres")
    if os.path.exists("assets/desenvolvimento.jpg"):
      st.image(
          "assets/desenvolvimento.jpg",
          caption="Anatomia 3D - Foco nos Deltóides",
          use_column_width=True,
        )
    else:
      st.warning(
          "⚠️ Imagem 'desenvolvimento.jpg' não encontrada na pasta 'assets'."
      )
    st.info(
        "🎯 **Como fazer (Iniciante):** Sentado no banco com apoio, segure os"
        " halteres na altura dos ombros e empurre para cima acima da cabeça."
    )

  else:
    ex_perna = st.selectbox(
        "Exercício:",
        [
            "Agachamento Livre",
            "Stiff com Barra",
            "Panturrilha em Pé na Máquina",
        ],
    )
    if "Agachamento" in ex_perna:
      st.markdown("#### 💥 Agachamento Livre")
      if os.path.exists("assets/agachamento.jpg"):
        st.image(
            "assets/agachamento.jpg",
            caption="Anatomia 3D - Foco em Quadríceps e Glúteos",
            use_column_width=True,
        )
      else:
        st.warning(
            "⚠️ Imagem 'agachamento.jpg' não encontrada na pasta 'assets'."
        )
      st.info(
          "🎯 **Como fazer (Iniciante):** Posicione a barra nos trapézios,"
          " desça o quadril jogando o bumbum para trás como se fosse sentar"
          " em uma cadeira, mantendo o calcanhar no chão."
      )
    elif "Stiff" in ex_perna:
      st.markdown("#### 💥 Stiff com Barra")
      if os.path.exists("assets/stiff.jpg"):
        st.image(
            "assets/stiff.jpg",
            caption="Anatomia 3D - Foco em Posteriores de Coxa",
            use_column_width=True,
        )
      else:
        st.warning("⚠️ Imagem 'stiff.jpg' não encontrada na pasta 'assets'.")
      st.info(
          "🎯 **Como fazer (Iniciante):** Pernas estendidas com leve flexão nos"
          " joelhos, desça a barra rente às pernas sentindo alongar a parte de"
          " trás da coxa."
      )
    else:
      st.markdown("#### 💥 Panturrilha em Pé na Máquina")
      if os.path.exists("assets/panturrilha.jpg"):
        st.image(
            "assets/panturrilha.jpg",
            caption="Anatomia 3D - Foco em Panturrilhas",
            use_column_width=True,
        )
      else:
        st.warning(
            "⚠️ Imagem 'panturrilha.jpg' não encontrada na pasta 'assets'."
        )
      st.info(
          "🎯 **Como fazer (Iniciante):** Apoie os ombros na máquina, deixe o"
          " calcanhar baixar para alongar bem embaixo e suba na ponta dos pés"
          " com força."
      )

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #707070; font-size: 0.8rem;'>Nutri"
    " Fit AI © 2026 - Alta Performance & Inteligência Artificial</p>",
    unsafe_allow_html=True,
)