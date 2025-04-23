
import openai
import pandas as pd
import requests
import os
from time import sleep

# 🔐 Sua chave da API da OpenAI
client = openai.OpenAI(api_key="")

# 📥 Arquivo CSV com os componentes
df = pd.read_csv("Componentes_Curriculares_Com_Imgslug.csv")

# 📁 Pasta onde as imagens serão salvas
os.makedirs("imagens_geradas", exist_ok=True)

# 🔄 Processar em blocos de 50
lote = 50
for inicio in range(0, len(df), lote):
    bloco = df.iloc[inicio:inicio + lote]

    print(f"🚀 Gerando imagens de {inicio+1} a {inicio+len(bloco)}...\n")

    for index, row in bloco.iterrows():
        slug = row["imgslug"]
        nome = row["Componente-curricular"]
        disciplina = row["Disciplina"]

        if os.path.exists(f"imagens_geradas/{slug}.png"):
            continue

        prompt = f"Conceptual illustration for high school {disciplina.lower()} about '{nome}', no text, neutral background, 512x512, semi-realistic style"

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1,
                response_format="url"
            )

            image_url = response.data[0].url
            image_data = requests.get(image_url).content

            with open(f"imagens_geradas/{slug}.png", "wb") as f:
                f.write(image_data)

            print(f"✅ {slug}.png gerada com sucesso.")
            sleep(2)

        except Exception as e:
            print(f"❌ Erro ao gerar imagem para {slug}: {e}")
            sleep(5)

    input("⏸️ Pressione Enter para continuar para o próximo bloco...")
