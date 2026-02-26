import os
import logging
import typer

from pathlib import Path
from moviepy.editor import VideoFileClip

from .text import Speech
from .video import MoviePyEditor, YoutubeVideo, YoutubeUpload
from .core import MontConcatStrategy, MontMidnightStrategy

app = typer.Typer(help="Canivete Suíço da edição de vídeos por linha de comando.")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.command()
def download(url: str, output: str = typer.Option(None, "-o", "--output", help="Caminho do arquivo de saída")):
    """Baixa vídeo do YouTube."""
    video = YoutubeVideo(url)
    video.save(path=output if output else None)


@app.command()
def cut(file: str, start:str, end:str, output: str = typer.Option("cutted/video_cut.mp4", "-o", "--output")):
    """Corta um vídeo com base em parâmetros start e end."""
    editor = MoviePyEditor(file)
    # cut_params = dict(param.split("=") for param in cut.split())
    editor.cut(start=start, end=end)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    editor.save(path=output)


@app.command()
def auto_legend(file: str, output: str = typer.Option("video_with_legends.mp4", "-o", "--output")):
    """Gera legendas automáticas para o vídeo."""
    logger.info("Iniciando processo de geração de legendas automáticas...")
    speech = Speech(href=file)
    segments = speech.segments()
    editor = MoviePyEditor(file)
    logger.info(f"Gerando legendas para {len(segments)} segmentos de áudio...")
    for segment in segments:
        logger.debug(f"Adicionando segmento |Start: {segment.start}, End: {segment.end}, Text: {segment.text}|")
        editor.add_legend(start=segment.start, end=segment.end, text=segment.text)
    logger.info("Legendas geradas, salvando vídeo com legendas...")
    editor.save(path=output)
    speech.close()
    editor.close()


@app.command()
def join(videos: str, output: str = typer.Option("video_joined.mp4", "-o", "--output")):
    """Concatena múltiplos vídeos."""
    concat_videos = videos.split(" ")
    logger.info(f"Concatenando vídeos: {concat_videos}")
    strategy = MontConcatStrategy(video_paths=concat_videos)
    strategy.save(output)
    strategy.close()
    logger.info("Vídeo concatenado salvo com sucesso.")


@app.command()
def midnight(videos: str, output: str = typer.Option("video_midnight.mp4", "-o", "--output")):
    """Aplica efeito 'midnight' em dois vídeos."""
    paths = videos.split(" ")
    video_superior = VideoFileClip(paths[0])
    video_inferior = VideoFileClip(paths[1])
    strategy = MontMidnightStrategy(video_paths=[video_superior, video_inferior])
    strategy.save(output)
    strategy.close()
    logger.info("Vídeo com efeito 'midnight' salvo com sucesso.")

@app.command()
def upload(
        video,
        titulo,
        descricao,
        privacy="public",
        category="Education",
        client_secrets = os.path.join(Path.home(), ".client_secrets.json"),
        credentials_file = os.path.join(Path.home(),".youtube-upload-credentials.json"),
    ):
    """Realiza o upload de vídeos no youtube."""
    logging.info("Realizando upload do seguinte arquivo: %s", video)
    YoutubeUpload.upload_video_to_youtube(
        video_path=video,
        title=titulo,
        description=descricao,
        privacy=privacy,
        category=category,
        client_secrets=client_secrets,
        credentials_file=credentials_file
    )
    logging.info("Upload realizado com sucesso!")

main = app
if __name__ == "__main__":
    main()