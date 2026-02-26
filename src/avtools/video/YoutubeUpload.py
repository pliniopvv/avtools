import os
import sys
from youtube_upload import main

def upload_video_to_youtube(
    video_path,
    title,
    description,
    category="Education",
    privacy="public",
    client_secrets=os.path.expanduser("~/.client_secrets.json"),
    credentials_file=os.path.expanduser("~/.youtube-upload-credentials.json")
):
    """
    Faz upload de um vídeo para o YouTube usando o projeto youtube-upload.
    """

    # Monta os argumentos como se fossem passados pela linha de comando
    args = [
        "--title", title,
        "--description", description,
        "--category", category,
        "--privacy", privacy,
        "--client-secrets", client_secrets,
        "--credentials-file", credentials_file,
        video_path,
    ]

    # Executa o upload usando a função principal do youtube-upload
    sys.argv = ["youtube-upload"] + args
    main.run()

# upload_video_to_youtube(
#     video_path="/home/gangss/Downloads/videos/cutted/video_cut.mp4",
#     title="Meu vídeo de teste",
#     description="Descrição do vídeo",
#     category="Education",
#     privacy="public"
# )
