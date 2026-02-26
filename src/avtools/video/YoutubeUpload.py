import sys
from youtube_upload import client
import typer

app = typer.Typer()

@app.command()
def realizar_upload():
    # Validação básica de argumentos
    if len(sys.argv) < 3:
        print("Uso: python app.py <caminho_video> <titulo> <descricao...>")
        sys.exit(1)

    # Captura dos argumentos
    video_path = sys.argv[1]
    video_title = sys.argv[2]
    video_description = " ".join(sys.argv[3:])

    # Configurações de autenticação
    client_secrets = "./client_secret_2.json"
    credentials_file = "./youtube-upload-credentials-pvpvv34.json"

    try:
        print(f"Iniciando upload para o YouTube: {video_title}...")

        # 1. Autenticação
        # O youtube-upload gerencia o fluxo de OAuth2 através destas funções:
        youtube = client.get_youtube_handler(client_secrets, credentials_file)

        # 2. Execução do Upload
        # Definimos os metadados do vídeo
        options = {
            "title": video_title,
            "description": video_description,
            "category": "Education", # Você pode mudar a categoria aqui
            "privacyStatus": "unlisted" # 'public', 'private' ou 'unlisted'
        }

        # Chama a função de upload da biblioteca
        video_id = client.upload(youtube, video_path, options)

        print(f"Sucesso! Vídeo enviado com ID: {video_id}")
        print(f"Link: https://www.youtube.com/watch?v={video_id}")

    except Exception as e:
        print(f"Ocorreu um erro durante o processo: {e}")

if __name__ == "__main__":
    realizar_upload()