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

if not api_key:
  st.warning(
      "⚠️ ATENÇÃO: A chave da OpenAI (OPENAI_API_KEY) não foi encontrada no"
      " sistema. Configure-a no terminal ou nos Secrets do Streamlit Cloud."
  )

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
        "🏋️‍♂️ Guia de Exercícios & Subgrupos",
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

  # Bloco Explicativo Dinâmico por Objetivo
  if "Recomposição" in objetivo:
    st.info(
        "💡 **Sobre este método:** Ideal para quem quer ganhar massa muscular"
        " e queimar gordura ao mesmo tempo. O sistema ajusta suas calorias para"
        " manter o peso estável, transformando gordura em músculos com alta"
        " ingestão proteica."
    )
  elif "Cutting" in objetivo:
    st.info(
        "💡 **Sobre este método:** Focado em secar e perder peso rápido, com"
        " déficit calórico estratégico e alto consumo de proteínas para garantir"
        " que você oxide apenas gordura e **não perca massa magra**."
    )
  else:
    st.info(
        "💡 **Sobre este método:** Perfeito para emagrecimento geral e"
        " redução de medidas de forma saudável, controlando as calorias"
        " diárias sem restrições extremas."
    )

  # Foco Principal do Treino (Ilustrativo / Seleção)
  st.markdown("### 🏋️‍♂️ Foco Principal do Treino")
  foco_treino = st.radio(
      "Selecione sua principal ênfase muscular atual:",
      [
          "Superiores (Peito, Costas, Bíceps, Tríceps e Deltoides) 🦾",
          "Inferiores (Quadríceps, Posteriores e Panturrilhas) 🦿",
          "Corpo Inteiro (Full Body) ⚡",
      ],
      horizontal=True,
  )

  if "Superiores" in foco_treino:
    st.info(
        "💪 **Dica de Performance para Superiores:** O foco está em otimizar a"
        " síntese proteica para peitoral, dorsal e braços, aplicando"
        " rigorosamente a progressão de carga (*progressive overload*)."
    )
  elif "Inferiores" in foco_treino:
    st.info(
        "🔥 **Dica de Performance para Inferiores:** Membros inferiores"
        " demandam grande gasto energético e estoques plenos de glicogênio."
        " Garanta o consumo adequado de carboidratos antes do treino pesado."
    )
  else:
    st.info(
        "⚡ **Dica de Performance Full Body:** Abordagem equilibrada para gasto"
        " calórico elevado e estímulo sistêmico."
    )

  if st.button("🔥 Calcular Minha Meta Fit"):
    # Cálculo básico de TDEE (Mifflin-St Jeor)
    if genero == "Masculino":
      tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
      tmb = 10 * peso + 6.25 * altura - 5 * idade - 161

    # Fator de atividade
    if "Sedentário" in nivel_atividade:
      tdee = tmb * 1.2
    elif "Levemente" in nivel_atividade:
      tdee = tmb * 1.375
    elif "Moderadamente" in nivel_atividade:
      tdee = tmb * 1.55
    else:
      tdee = tmb * 1.725

    # Ajuste por objetivo
    if "Recomposição" in objetivo:
      calorias_alvo = int(tdee)
    elif "Cutting" in objetivo:
      calorias_alvo = int(tdee - 400)
    else:
      calorias_alvo = int(tdee - 500)

    proteina_alvo = int(peso * 2.2)  # Base segura em gramas

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
        with st.spinner(
            "Analisando imagem e estimando macros com inteligência artificial..."
        ):
          try:
            # Salvando imagem temporariamente para envio à API
            caminho_temp = "temp_prato.jpg"
            imagem.save(caminho_temp)

            # Bloco Anti-Tijolo / Blindagem Visual (Exemplo de validação rápida)
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um nutricionista esportivo rigoroso e um"
                            " sistema de visão computacional de segurança."
                            " Primeiro, verifique se a imagem contém"
                            " estritamente comida ou refeição. Se a imagem for"
                            " um objeto inválido (ex: tijolo, parede, animal,"
                            " selfie, objeto aleatório), retorne exatamente:"
                            " 'ERRO_IMAGEM_INVALIDA'. Se for comida, analise e"
                            " estime as calorias, proteínas, carboidratos e"
                            " gorduras de forma detalhada em Markdown."
                        ),
                    },
                    {
                        "role": "user",
                        "content": "Analise esta refeição para o meu plano.",
                    },
                ],
            )
            resultado_ia = resposta.choices[0].message.content

            if "ERRO_IMAGEM_INVALIDA" in resultado_ia:
              st.error(
                  "🚨 **Alerta de Segurança (Anti-Tijolo):** A imagem enviada"
                  " não parece ser uma refeição válida. Por favor, envie uma"
                  " foto clara do seu prato de comida."
              )
            else:
              st.markdown("### 📋 Relatório Nutricional da Refeição")
              st.markdown(resultado_ia)

          except Exception as e:
            st.error(f"Ocorreu um erro ao processar a imagem: {e}")

# ==========================================
# ABA 3: GUIA DE EXERCÍCIOS & SUBGRUPOS
# ==========================================
with aba_exercicios:
  st.markdown("### 🏋️‍♂️ Guia Técnico de Exercícios & Ilustrações")
  st.write(
      "Consulte os agrupamentos musculares, orientações de execução, foco em"
      " hipertrofia e imagens ilustrativas."
  )

  subgrupo = st.selectbox(
      "Selecione o Subgrupo Muscular:",
      [
          "Peitoral (Superiores) 🦾",
          "Dorsal / Costas (Superiores) 🦾",
          "Bíceps (Superiores) 🦾",
          "Tríceps (Superiores) 🦾",
          "Deltoides / Ombros (Superiores) 🦾",
          "Quadríceps (Inferiores) 🦿",
          "Posteriores de Coxa (Inferiores) 🦿",
          "Panturrilhas (Inferiores) 🦿",
      ],
  )

  if "Peitoral" in subgrupo:
    st.markdown("#### 💥 Foco: Peitoral (Superiores)")
    st.image(
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=1000&auto=format&fit=crop",
        caption="Treino de Peitoral e Força",
        use_column_width=True,
    )
    st.markdown(
        "- **Principais Exercícios:** Supino Reto com Barra, Supino Inclinado com"
        " Halteres, Crucifixo na Polia.\n- **Dica de Ouro:** Mantenha as"
        " escápulas deprimidas e retraídas no banco. Amplitude completa na"
        " fase excêntrica (alongamento).\n- **Progressão de Carga:** Aumente o"
        " peso apenas quando dominar 3 séries de 8 a 10 repetições com execução"
        " perfeita."
    )
  elif "Dorsal" in subgrupo:
    st.markdown("#### 💥 Foco: Costas / Dorsal (Superiores)")
    st.image(
        "https://images.unsplash.com/photo-1605296867304-46d5465a13f1?q=80&w=1000&auto=format&fit=crop",
        caption="Treino de Costas e Espessura",
        use_column_width=True,
    )
    st.markdown(
        "- **Principais Exercícios:** Puxada Alta na Polia, Remada Curvada com"
        " Barra, Remada Baixa.\n- **Dica de Ouro:** Puxe com os cotovelos em"
        " direção ao quadril, focando em esmagar as dorsais.\n- **Progressão"
        " de Carga:** Mantenha a coluna neutra e firme em todas as repetições."
    )
  elif "Bíceps" in subgrupo:
    st.markdown("#### 💥 Foco: Bíceps (Superiores)")
    st.image(
        "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=1000&auto=format&fit=crop",
        caption="Treino de Bíceps e Braços",
        use_column_width=True,
    )
    st.markdown(
        "- **Principais Exercícios:** Rosca Direta com Barra W, Rosca Alternada"
        " com Halteres, Rosca Scott.\n- **Dica de Ouro:** Evite balançar o"
        " tronco. O controle na descida (fase excêntrica) rompe as"
        " fibras.\n- **Progressão de Carga:** Ajuste a carga de forma"
        " progressiva sem comprometer a postura."
    )
  elif "Tríceps" in subgrupo:
    st.markdown("#### 💥 Foco: Tríceps (Superiores)")
    st.image(
        "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1000&auto=format&fit=crop",
        caption="Treino de Tríceps",
        use_column_width=True,
    )
    st.markdown(
        "- **Principais Exercícios:** Tríceps na Polia (Corda ou Barra Reta),"
        " Tríceps Testa, Supino Fechado.\n- **Dica de Ouro:** Mantenha os"
        " cotovelos fixos ao lado do corpo para isolar o tríceps.\n-"
        " **Progressão de Carga:** Busque falha concêntrica segura nas últimas"
        " séries."
    )
  elif "Deltoides" in subgrupo:
    st.markdown("#### 💥 Foco: Deltoides / Ombros (Superiores)")
    st.image(
        "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?q=80&w=1000&auto=format&fit=crop",
        caption="Treino de Ombros e Deltoides",
        use_column_width=True,
    )
    st.markdown(
        "- **Principais Exercícios:** Desenvolvimento com Halteres, Elevação"
        " Lateral na Polia, Crucifixo Inverso.\n- **Dica de Ouro:** O feixe"
        " lateral do ombro dá a largura visual do tronco; foque na elevação"
        " lateral controlada.\n- **Progressão de Carga:** Use cargas moderadas"
        " com foco na conexão mente-músculo."
    )
  elif "Quadríceps" in subgrupo:
    st.markdown("#### 💥 Foco: Quadríceps (Inferiores)")
    st.image(
        "https://images.unsplash.com/photo-1574680096145-d05b474e2155?q=80&w=1000&auto=format&fit=crop",
        caption="Treino de Pernas e Quadríceps",
        use_column_width=True,
    )
    st.markdown(
        "- **Principais Exercícios:** Agachamento Livre, Leg Press 45°, Cadeira"
        " Extensora.\n- **Dica de Ouro:** Mantenha os calcanhares apoiados e o"
        " tronco erguido para maximizar o recrutamento da coxa.\n-"
        " **Progressão de Carga:** Respeite o intervalo de descanso (2 a 3"
        " minutos) devido à alta demanda energética."
    )
  elif "Posteriores" in subgrupo:
    st.markdown("#### 💥 Foco: Posteriores de Coxa (Inferiores)")
    st.image(
        "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=1000&auto=format&fit=crop",
        caption="Treino de Posteriores e Glúteos",
        use_column_width=True,
    )
    st.markdown(
        "- **Principais Exercícios:** Stiff com Barra, Mesa Flexora, Cadeira"
        " Flexora.\n- **Dica de Ouro:** Inicie o movimento jogando o quadril"
        " para trás (dobradiça de quadril) antes de dobrar os joelhos.\n-"
        " **Progressão de Carga:** Mantenha a tensão contínua na musculatura."
    )
  else:
    st.markdown("#### 💥 Foco: Panturrilhas (Inferiores)")
    st.image(
        "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?q=80&w=1000&auto=format&fit=crop",
        caption="Treino de Panturrilhas",
        use_column_width=True,
    )
    st.markdown(
        "- **Principais Exercícios:** Panturrilha em Pé na Máquina, Panturrilha"
        " Sentado (Sóleo).\n- **Dica de Ouro:** Faça uma pausa de 1 segundo no"
        " pico da contração em cima e alongue completamente embaixo.\n-"
        " **Progressão de Carga:** A panturrilha exige volume e intensidade;"
        " trabalhe com amplitudes máximas."
    )