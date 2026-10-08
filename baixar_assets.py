import os
import requests

# Dicionário com os links diretos das ilustrações anatômicas oficiais para cada exercício
exercicios_imagens = {
    "supino_reto.jpg": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=1000&auto=format&fit=crop",
    "supino_inclinado.jpg": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?q=80&w=1000&auto=format&fit=crop",
    "crucifixo.jpg": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1000&auto=format&fit=crop",
    "puxada_alta.jpg": "https://images.unsplash.com/photo-1605296867304-46d5465a13f1?q=80&w=1000&auto=format&fit=crop",
    "remada_curvada.jpg": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=1000&auto=format&fit=crop",
    "rosca_direta.jpg": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=1000&auto=format&fit=crop",
    "triceps_polia.jpg": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1000&auto=format&fit=crop",
    "desenvolvimento.jpg": "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?q=80&w=1000&auto=format&fit=crop",
    "agachamento.jpg": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?q=80&w=1000&auto=format&fit=crop",
    "stiff.jpg": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=1000&auto=format&fit=crop",
    "panturrilha.jpg": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?q=80&w=1000&auto=format&fit=crop"
}

# Nome da pasta de destino
pasta_assets = "assets"

# Cria a pasta assets se não existir
if not os.path.exists(pasta_assets):
    os.makedirs(pasta_assets)
    print(f"📁 Pasta '{pasta_assets}' criada com sucesso!")

print("🚀 Iniciando o download dos modelos e ilustrações em lote...")

# Loop para baixar cada imagem
for nome_arquivo, url in exercicios_imagens.items():
    caminho_completo = os.path.join(pasta_assets, nome_arquivo)
    try:
        resposta = requests.get(url, timeout=10)
        if resposta.status_code == 200:
            with open(caminho_completo, "wb") as f:
                f.write(resposta.content)
            print(f"✅ Baixado com sucesso: {nome_arquivo}")
        else:
            print(f"⚠️ Erro ao baixar {nome_arquivo} (Status: {resposta.status_code})")
    except Exception as e:
        print(f"❌ Falha na conexão para {nome_arquivo}: {e}")

print("🎯 Processo finalizado! Todas as imagens estão prontas na pasta assets.")