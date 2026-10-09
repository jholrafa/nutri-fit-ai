from datetime import datetime
import os
import base64
import io
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

# Inicialização Blindada do Cliente OpenAI (Local e Nuvem)
api_key = None
try:
  if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
  pass

if not api_key:
  api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None

# Inicializar o Session State para o Controle de Acesso e Histórico
if "usuario_logado" not in st.session_state:
  st.session_state.usuario_logado = False
if "email_usuario" not in st.session_state:
  st.session_state.email_usuario = ""
if "plano_ativo" not in st.session_state:
  st.session_state.plano_ativo = False

if "historico_refeicoes" not in st.session_state:
  st.session_state.historico_refeicoes = []
if "calorias_meta" not in st.session_state:
  st.session_state.calorias_meta = 2000
if "proteina_meta" not in st.session_state:
  st.session_state.proteina_meta = 160

# ==========================================
# BARREIRA 1: TELA DE LOGIN / CADASTRO
# ==========================================
if not st.session_state.usuario_logado:
  st.markdown(
      "<h2 style='text-align: center;'>🔐 Acesso Restrito - Nutri Fit AI</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center;'>Faça login ou cadastre-se para acessar"
      " seu personal e nutricionista na nuvem.</p>",
      unsafe_allow_html=True,
  )

  tab_login, tab_cadastro = st.tabs(["🔑 Entrar", "📝 Criar Conta"])

  with tab_login:
    st.markdown("### Acesse sua conta")
    email_login = st.text_input("E-mail", key="login_email")
    senha_login = st.text_input("Senha", type="password", key="login_senha")

    if st.button("🚀 Entrar no App"):
      if email_login.strip() != "":
        st.session_state.usuario_logado = True
        st.session_state.email_usuario = email_login
        st.success("Login realizado com sucesso!")
        st.rerun()
      else:
        st.error("Por favor, digite seu e-mail.")

  with tab_cadastro:
    st.markdown("### Crie sua conta e comece agora")
    nome_cad = st.text_input("Nome Completo")
    email_cad = st.text_input("E-mail", key="cad_email")
    senha_cad = st.text_input("Senha", type="password", key="cad_senha")

    if st.button("✨ Cadastrar e Ir para os Planos"):
      if email_cad.strip() != "" and senha_cad.strip() != "":
        st.session_state.usuario_logado = True
        st.session_state.email_usuario = email_cad
        st.success("Conta criada! Redirecionando para seleção de planos...")
        st.rerun()
      else:
        st.error("Preencha todos os campos para continuar.")

  st.stop()

# ==========================================
# BARREIRA 2: TELA DE SELEÇÃO DE PLANOS & PIX
# ==========================================
if not st.session_state.plano_ativo:
    st.markdown(
        "<h2 style='text-align: center;'>💳 Checkout & Planos - Nutri Fit AI</h2>",
        unsafe_allow_html=True,
    )
    st.info(
        "Escolha o seu plano abaixo e finalize o pagamento com total segurança através da Stripe:"
    )

    aba_varejo, aba_b2b = st.tabs(
        [
            "🛍️ Plano Varejo (R$ 49,90/mês)",
            "🏢 Licença B2B Academias (R$ 297,00/mês)",
        ]
    )

    with aba_varejo:
        st.markdown("### 🔥 Plano Aluno Fit - Individual")
        st.markdown(
            "- ✅ Scanner Ilimitado de Refeições por IA\n- ✅ Controle de Macros e Painel Diário\n- ✅ Guia Master de Exercícios 3D"
        )
        st.markdown("#### 💰 Valor: **R$ 49,90 / mês**")
        st.markdown("---")
        st.markdown("#### 🚀 Pagamento Seguro via Stripe (Pix ou Cartão)")
        st.write(
            "Clique no botão abaixo para abrir a página oficial de pagamento da Stripe:"
        )

        # Botão oficial da Stripe para o Plano Varejo
        st.link_button(
            "Assinar Plano Varejo (Stripe)", 
            "https://buy.stripe.com/6oU8wO65b6Km4WJ6Fzd3i00",
            use_container_width=True
        )

    with aba_b2b:
        st.markdown("### 🏢 Licença Corporativa - Academias & Personals")
        st.markdown(
            "- ✅ Até 30 Acessos Simultâneos para Alunos\n- ✅ Scanner de IA Prioritário\n- ✅ Suporte Exclusivo e Gestão de Alunos"
        )
        st.markdown("#### 💰 Valor: **R$ 297,00 / mês**")
        st.markdown("---")
        st.markdown("#### 🤝 Atendimento Comercial Exclusivo")
        st.write(
            "Para fechar a licença corporativa da academia com negociação personalizada, fale direto com nossa equipe:"
        )
        st.info("Entre em contato pelo atendimento direto para liberação da chave mestra da academia.")

    st.markdown("---")
    if st.button("🚪 Sair / Trocar de Conta"):
        st.session_state.usuario_logado = False
        st.session_state.email_usuario = ""
        st.rerun()

    st.stop()

# ==========================================
# APLICATIVO PRINCIPAL (APÓS LOGIN E PAGAMENTO)
# ==========================================

# Dicionário de dias da semana em português
dias_semana_pt = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}

dia_ingles = datetime.now().strftime("%A")
dia_atual = dias_semana_pt.get(dia_ingles, dia_ingles)
data_hoje = datetime.now().strftime("%d/%m/%Y")

# Cabeçalho com botão de Logout
col_topo1, col_topo2 = st.columns([0.8, 0.2])
with col_topo1:
  st.markdown(
      "<h1 style='text-align: left;'>⚡ Nutri Fit AI</h1>",
      unsafe_allow_html=True,
  )
with col_topo2:
  if st.button("🚪 Sair"):
    st.session_state.usuario_logado = False
    st.session_state.plano_ativo = False
    st.rerun()

st.markdown(
    f"<h5 style='color: #00FF66;'>📅 {dia_atual}, {data_hoje} | Logado como:"
    f" <b>{st.session_state.email_usuario}</b></h5>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Abas de Navegação do Aplicativo
aba_metas, aba_scanner, aba_exercicios = st.tabs(
    [
        "📊 Definir Metas & Dieta",
        "📸 Scanner por Câmera & Histórico (IA)",
        "🏋️‍♂️ Guia Master de Exercícios & Anatomia 3D",
    ]
)

# ==========================================
# ABA 1: METAS & DIETA
# ==========================================
with aba_metas:
  st.markdown("### 🎛️ Defina suas Metas e Perfil")
  st.write(
      "Preencha seus dados para calcularmos seu TDEE, macros ideias e a meta"
      " diária."
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

  if st.button("🔥 Calcular e Salvar Minha Meta Diária"):
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

    st.session_state.calorias_meta = calorias_alvo
    st.session_state.proteina_meta = proteina_alvo

    st.success("🎯 Metas Atualizadas com Sucesso para o seu dia!")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Gasto Diário (TDEE)", f"{int(tdee)} kcal")
    col_m2.metric("Sua Meta Calórica", f"{calorias_alvo} kcal")
    col_m3.metric("Meta de Proteína", f"{proteina_alvo} g/dia")

# ==========================================
# ABA 2: SCANNER, HISTÓRICO, CÂMERA & ACUMULADOR
# ==========================================
with aba_scanner:
  st.markdown("### 📸 Scanner Inteligente por Câmera & Histórico de Hoje")
  st.write(
      "Tire a foto da refeição direto pela câmera ou envie um arquivo. A IA"
      " conta os pedaços e acumula no seu dia."
  )

  total_calorias_consumidas = sum(
      [r["calorias"] for r in st.session_state.historico_refeicoes]
  )
  total_proteinas_consumidas = sum(
      [r["proteina"] for r in st.session_state.historico_refeicoes]
  )

  meta_c = st.session_state.calorias_meta
  meta_p = st.session_state.proteina_meta

  st.markdown("---")
  st.markdown(f"#### 📊 Painel Diário: {dia_atual}")
  col_p1, col_p2 = st.columns(2)
  col_p1.metric(
      "Calorias Consumidas / Meta",
      f"{total_calorias_consumidas} / {meta_c} kcal",
  )
  col_p2.metric(
      "Proteínas Consumidas / Meta",
      f"{total_proteinas_consumidas}g / {meta_p}g",
  )

  diferenca_calorias = meta_c - total_calorias_consumidas
  if total_calorias_consumidas == 0:
    st.info(
        "💡 **Status:** Nenhuma refeição registrada hoje. Tire a foto da sua"
        " primeira refeição abaixo!"
    )
  elif diferenca_calorias > 300:
    st.info(
        f"🔥 **Alerta Nutricional:** Faltam cerca de {diferenca_calorias} kcal"
        " para atingir sua meta de hoje. Continue firme!"
    )
  elif 0 <= diferenca_calorias <= 300:
    st.success(
        "🎯 **Alerta Nutricional:** Você está bem próximo da sua meta calórica"
        " diária! Excelente controle."
    )
  else:
    excesso = abs(diferenca_calorias)
    st.warning(
        f"⚠️ **Alerta Nutricional:** Atenção! Você ultrapassou a meta de hoje"
        " em {excesso} kcal."
    )
  st.markdown("---")

  modo_captura = st.radio(
      "Como deseja enviar a foto?",
      ["📷 Tirar foto com a Câmera ao Vivo", "📁 Enviar arquivo de imagem"],
  )

  imagem_para_analise = None

  if modo_captura == "📷 Tirar foto com a Câmera ao Vivo":
    imagem_camera = st.camera_input("Posicione o prato e clique em 'Tirar foto'")
    if imagem_camera is not None:
      imagem_para_analise = Image.open(imagem_camera)
  else:
    arquivo_foto = st.file_uploader(
        "Escolha o arquivo de foto...", type=["jpg", "jpeg", "png"]
    )
    if arquivo_foto is not None:
      imagem_para_analise = Image.open(arquivo_foto)

  if imagem_para_analise is not None:
    st.image(
        imagem_para_analise,
        caption="Refeição capturada para análise da IA",
        use_container_width=True,
    )

    if st.button("🔍 Analisar Prato e Adicionar ao Histórico do Dia"):
      if not client:
        st.error(
            "Erro: Chave da OpenAI não configurada. Verifique os Secrets."
        )
      else:
        with st.spinner(
            "IA contando os pedaços e calculando os macros totais..."
        ):
          try:
            buffered = io.BytesIO()
            imagem_para_analise.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um nutricionista esportivo rigoroso. Analise"
                            " a foto do alimento enviado. **CONTE visualmente"
                            " quantos pedaços, unidades ou porções existem no"
                            " prato ou recipiente** (por exemplo: se houver 4"
                            " pedaços de frango, calcule o total somando os 4"
                            " pedaços). Estime as calorias totais e as"
                            " proteínas totais de TUDO o que está visível na"
                            " imagem. Forneça o parecer nutricional em Markdown"
                            " detalhando a quantidade contada e, obrigatoriamente,"
                            " no final de tudo, escreva exatamente assim em"
                            " duas linhas separadas:\nCALORIAS: [número total]\nPROTEINA:"
                            " [número total]"
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Analise este alimento, conte os pedaços"
                                    " presentes e forneça o total de macros"
                                    " estimados."
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_str}"
                                },
                            },
                        ],
                    },
                ],
            )
            resultado_ia = resposta.choices[0].message.content

            import re

            calorias_detectadas = 200
            proteina_detectada = 2

            match_cals = re.search(
                r"CALORIAS:\s*(\d+)", resultado_ia, re.IGNORECASE
            )
            match_prot = re.search(
                r"PROTEINA:\s*(\d+)", resultado_ia, re.IGNORECASE
            )

            if match_cals:
              calorias_detectadas = int(match_cals.group(1))
            if match_prot:
              proteina_detectada = int(match_prot.group(1))

            horario_atual = datetime.now().strftime("%H:%M")

            st.session_state.historico_refeicoes.append({
                "horario": horario_atual,
                "descricao": "Refeição Escaneada pela IA",
                "calorias": calorias_detectadas,
                "proteina": proteina_detectada,
            })

            st.success(f"✅ Refeição registrada com sucesso às {horario_atual}!")
            st.markdown("### 📋 Parecer do Nutri AI")
            st.markdown(resultado_ia)
            st.rerun()
          except Exception as e:
            st.error(f"Erro ao processar com IA: {e}")

  st.markdown("### 📜 Histórico de Refeições de Hoje")
  if len(st.session_state.historico_refeicoes) == 0:
    st.write("Nenhuma refeição no histórico de hoje ainda.")
  else:
    for idx, ref in enumerate(st.session_state.historico_refeicoes):
      col_item1, col_item2 = st.columns([0.8, 0.2])
      with col_item1:
        st.markdown(
            f"**{idx+1}. Horário:** {ref['horario']} | **Calorias:**"
            f" `{ref['calorias']} kcal` | **Proteína:** `{ref['proteina']}g`"
        )
      with col_item2:
        if st.button("🗑️", key=f"del_ref_{idx}"):
          st.session_state.historico_refeicoes.pop(idx)
          st.rerun()

    if st.button("🗑️ Limpar Histórico do Dia Inteiro"):
      st.session_state.historico_refeicoes = []
      st.rerun()

# ==========================================
# ABA 3: GUIA MASTER DE EXERCÍCIOS & ANATOMIA 3D
# ==========================================
with aba_exercicios:
  st.markdown("### 🏋️‍♂️ Guia Master de Exercícios & Anatomia 3D")
  st.write(
      "Selecione o grupo e o exercício para ver a ilustração anatômica e a"
      " execução."
  )

  grupo_muscular = st.selectbox(
      "Selecione o Grupo Muscular:",
      [
          "Peitoral (Supinos, Halteres, Polia & Livres) 🦾",
          "Costas / Dorsal (Puxadas, Remadas & Barra) 🦾",
          "Braços (Bíceps e Tríceps - Completo) 🦾",
          "Ombros (Deltoides - Livres & Polia) 🦾",
          "Membros Inferiores (Pernas e Máquinas) 🦿",
      ],
  )


  def exibir_foto_exercicio(nome_arquivo, caption_texto):
    caminho = os.path.join("assets", nome_arquivo)
    if os.path.exists(caminho):
      st.image(caminho, caption=caption_texto, use_container_width=True)
    else:
      st.warning(
          f"⚠️ Imagem '{nome_arquivo}' não encontrada na pasta 'assets'."
      )


  if "Peitoral" in grupo_muscular:
    ex_peito = st.selectbox(
        "Exercício:",
        [
            "Supino Reto com Barra",
            "Supino Inclinado com Halteres",
            "Crossover / Polia Alta",
            "Flexão de Braço Tradicional",
            "Crucifixo com Halteres no Banco Reto",
        ],
    )

    if "Supino Reto" in ex_peito:
      st.markdown("#### 💥 Supino Reto com Barra")
      exibir_foto_exercicio(
          "supino_reto.jpg", "Anatomia 3D - Peitoral e Tríceps"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Deite no banco, pés firmes no chão,"
          " escápulas retraídas. Desça a barra controlando até a linha do"
          " peito e empurre para cima."
      )
    elif "Inclinado" in ex_peito:
      st.markdown("#### 💥 Supino Inclinado com Halteres")
      exibir_foto_exercicio(
          "supino_inclinado.jpg", "Anatomia 3D - Peitoral Superior"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Banco a 30°-45°. Controle a descida dos"
          " halteres alongando a parte superior do peito e contraia no topo."
      )
    elif "Crossover" in ex_peito:
      st.markdown("#### 💥 Crossover / Polia Alta")
      exibir_foto_exercicio("crossover.jpg", "Anatomia 3D - Feixe Sternal")
      st.info(
          "🎯 **Execução (Iniciante):** Em pé no centro dos cabos altos,"
          " tronco levemente inclinado à frente, cruze os cabos na altura"
          " do abdômen inferior esmagando o peito."
      )
    elif "Flexão" in ex_peito:
      st.markdown("#### 💥 Flexão de Braço Tradicional")
      exibir_foto_exercicio(
          "flexao_braco.jpg", "Anatomia 3D - Peitoral e Core"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Mantenha o corpo alinhado, abdômen"
          " contraído, desça o peito próximo ao solo e empurre."
      )
    else:
      st.markdown("#### 💥 Crucifixo com Halteres no Banco Reto")
      exibir_foto_exercicio(
          "crucifixo_halter.jpg", "Anatomia 3D - Isolamento Peitoral"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Deitado no banco reto, braços levemente"
          " flexionados, abra os halteres sentindo alongar o peitoral e feche"
          " em abraço."
      )

  elif "Costas" in grupo_muscular:
    ex_costas = st.selectbox(
        "Exercício:",
        [
            "Puxada Alta na Polia / Pulldown",
            "Remada Curvada com Barra",
            "Remada Baixa na Polia / Triângulo",
            "Barra Fixa Pronada / Supinada",
        ],
    )
    if "Puxada Alta" in ex_costas:
      st.markdown("#### 💥 Puxada Alta na Polia / Pulldown")
      exibir_foto_exercicio("puxada_alta.jpg", "Anatomia 3D - Grande Dorsal")
      st.info(
          "🎯 **Execução (Iniciante):** Sente com joelhos travados, puxe a barra"
          " em direção ao peito estufando o tronco e puxando com os cotovelos"
          " para baixo."
      )
    elif "Remada Curvada" in ex_costas:
      st.markdown("#### 💥 Remada Curvada com Barra")
      exibir_foto_exercicio(
          "remada_curvada.jpg", "Anatomia 3D - Espessura de Dorsal"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Tronco inclinado a 45°, coluna neutra,"
          " puxe a barra em direção ao umbigo."
      )
    elif "Remada Baixa" in ex_costas:
      st.markdown("#### 💥 Remada Baixa na Polia / Triângulo")
      exibir_foto_exercicio(
          "remada_baixa.jpg", "Anatomia 3D - Meio das Costas na Polia"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Coluna reta, puxe o triângulo até o"
          " abdômen mantendo o controle total na volta."
      )
    else:
      st.markdown("#### 💥 Barra Fixa Pronada / Supinada")
      exibir_foto_exercicio("barra_fixa.jpg", "Anatomia 3D - Dorsal e Bíceps")
      st.info(
          "🎯 **Execução (Iniciante):** Puxe o corpo para cima até o queixo"
          " ultrapassar a barra, controlando a descida."
      )

  elif "Braços" in grupo_muscular:
    ex_braco = st.selectbox(
        "Exercício:",
        [
            "Rosca Direta com Barra W",
            "Rosca Alternada com Halteres",
            "Tríceps na Polia com Corda",
            "Tríceps Testa com Barra W",
            "Paralelas no Apoio / Supino Fechado",
        ],
    )
    if "Rosca Direta" in ex_braco:
      st.markdown("#### 💥 Rosca Direta com Barra W")
      exibir_foto_exercicio("rosca_direta.jpg", "Anatomia 3D - Bíceps Braquial")
      st.info(
          "🎯 **Execução (Iniciante):** Cotovelos colados nas costelas, suba a"
          " barra sem balançar o tronco."
      )
    elif "Rosca Alternada" in ex_braco:
      st.markdown("#### 💥 Rosca Alternada com Halteres")
      exibir_foto_exercicio(
          "rosca_alternada.jpg", "Anatomia 3D - Bíceps e Antebraço"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Alterne os braços fazendo supinação no"
          " topo."
      )
    elif "Tríceps na Polia" in ex_braco:
      st.markdown("#### 💥 Tríceps na Polia com Corda")
      exibir_foto_exercicio(
          "triceps_polia.jpg", "Anatomia 3D - Tríceps (Cabeças)"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Cotovelos fixos ao lado do corpo,"
          " empurre para baixo abrindo as pontas da corda no final."
      )
    elif "Tríceps Testa" in ex_braco:
      st.markdown("#### 💥 Tríceps Testa com Barra W")
      exibir_foto_exercicio(
          "triceps_testa.jpg", "Anatomia 3D - Tríceps (Cabeça Longa)"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Deitado no banco, flexione os cotovelos"
          " levando a barra em direção à testa e estenda."
      )
    else:
      st.markdown("#### 💥 Paralelas no Apoio / Supino Fechado")
      exibir_foto_exercicio(
          "paralelas.jpg", "Anatomia 3D - Tríceps e Peitoral"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Projete o tronco levemente à frente,"
          " desça controlando o peso e empurre para cima."
      )

  elif "Ombros" in grupo_muscular:
    ex_ombro = st.selectbox(
        "Exercício:",
        [
            "Desenvolvimento com Halteres",
            "Elevação Lateral com Halteres / Polia",
            "Desenvolvimento Militar com Barra",
        ],
    )
    if "Desenvolvimento com Halteres" in ex_ombro:
      st.markdown("#### 💥 Desenvolvimento com Halteres")
      exibir_foto_exercicio("desenvolvimento.jpg", "Anatomia 3D - Deltóides")
      st.info(
          "🎯 **Execução (Iniciante):** Sentado com apoio, halteres na altura"
          " dos ombros, empurre para cima acima da cabeça."
      )
    elif "Elevação Lateral" in ex_ombro:
      st.markdown("#### 💥 Elevação Lateral com Halteres / Polia")
      exibir_foto_exercicio(
          "elevacao_lateral.jpg", "Anatomia 3D - Deltóide Lateral"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Em pé, levante os pesos lateralmente até"
          " a altura dos ombros com leve flexão nos cotovelos."
      )
    else:
      st.markdown("#### 💥 Desenvolvimento Militar com Barra")
      exibir_foto_exercicio(
          "desenvolvimento_barra.jpg", "Anatomia 3D - Deltoide Anterior e Core"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Empurre a barra por cima da cabeça"
          " mantendo o abdômen contraído."
      )

  else:
    ex_perna = st.selectbox(
        "Exercício:",
        [
            "Agachamento Livre com Barra",
            "Leg Press 45°",
            "Cadeira Extensora",
            "Stiff com Barra / Halteres",
            "Mesa Flexora",
            "Afundo / Passada com Halteres",
            "Panturrilha em Pé na Máquina",
        ],
    )
    if "Agachamento" in ex_perna:
      st.markdown("#### 💥 Agachamento Livre com Barra")
      exibir_foto_exercicio("agachamento.jpg", "Anatomia 3D - Quadríceps e Glúteos")
      st.info(
          "🎯 **Execução (Iniciante):** Posicione a barra nos trapézios,"
          " desça o quadril jogando o bumbum para trás com calcanhares firmes"
          " no chão."
      )
    elif "Leg Press" in ex_perna:
      st.markdown("#### 💥 Leg Press 45°")
      exibir_foto_exercicio("leg_press.jpg", "Anatomia 3D - Quadríceps")
      st.info(
          "🎯 **Execução (Iniciante):** Pés na largura dos ombros na plataforma,"
          " desça controlando sem tirar a lombar do encosto."
      )
    elif "Cadeira Extensora" in ex_perna:
      st.markdown("#### 💥 Cadeira Extensora")
      exibir_foto_exercicio(
          "cadeira_extensora.jpg", "Anatomia 3D - Isolamento Quadríceps"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Sente com o joelho alinhado ao eixo,"
          " estenda a perna completamente e segure 1 segundo no topo."
      )
    elif "Stiff" in ex_perna:
      st.markdown("#### 💥 Stiff com Barra / Halteres")
      exibir_foto_exercicio("stiff.jpg", "Anatomia 3D - Posteriores de Coxa")
      st.info(
          "🎯 **Execução (Iniciante):** Pernas semi-estendidas, faça a"
          " dobradiça de quadril descendo o peso rente às pernas."
      )
    elif "Mesa Flexora" in ex_perna:
      st.markdown("#### 💥 Mesa Flexora")
      exibir_foto_exercicio(
          "mesa_flexora.jpg", "Anatomia 3D - Isquiotibiais"
      )
      st.info(
          "🎯 **Execução (Iniciante):** Deitado de bruços, flexione os joelhos"
          " puxando o calcanhar em direção aos glúteos."
      )
    elif "Afundo" in ex_perna:
      st.markdown("#### 💥 Afundo / Passada com Halteres")
      exibir_foto_exercicio("afundo.jpg", "Anatomia 3D - Pernas e Equilíbrio")
      st.info(
          "🎯 **Execução (Iniciante):** Dê um passo à frente e flexione ambos"
          " os joelhos em 90 graus, mantendo o tronco erguido."
      )
    else:
      st.markdown("#### 💥 Panturrilha em Pé na Máquina")
      exibir_foto_exercicio("panturrilha.jpg", "Anatomia 3D - Panturrilhas")
      st.info(
          "🎯 **Execução (Iniciante):** Apoie os ombros na máquina, deixe o"
          " calcanhar baixar para alongar bem embaixo e suba na ponta dos pés."
      )

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #707070; font-size: 0.8rem;'>Nutri"
    " Fit AI © 2026 - Alta Performance & Inteligência Artificial</p>",
    unsafe_allow_html=True,
)