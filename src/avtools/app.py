import argparse
from dataclasses import asdict
from pprint import pprint
from moviepy.editor import VideoFileClip, concatenate_videoclips

from .text import Speech
from .video import MoviePyEditor, YoutubeVideo
from .core import MontConcatStrategy, MontMidnightStrategy

import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main():
    parser = argparse.ArgumentParser(description="Canivete Suíço da edição vídeos em geral por linha de comandos.")
    
    parser.add_argument("-d", "--download", default=None, help="URL do vídeo a ser processado.")
    parser.add_argument("-F", "--file", default=None, help="Caminho do arquivo de vídeo a ser editado.")
    parser.add_argument("-al", "--auto-legend", action="store_true", help="Gera legendas automáticas para o vídeo.")
    parser.add_argument("-o", "--output", default=None, help="Caminho do arquivo de saída.")

    parser.add_argument("-v", "--version", action="version", version="avtools 0.1.0")

    parser.add_argument("--cut", default=None, help="Corta o vídeo de acordo com os parâmetros informados. Exemplo: --cut \"start=00:01:00 end=00:02:00\"")

    parser.add_argument("--effect", action="store_true", help="Ativa o modo de edição interativa do vídeo. (Em desenvolvimento)")
    parser.add_argument("--join", default=None, help="Concatena múltiplos vídeos. Exemplo: --join \"video1.mp4 video2.mp4 video3.mp4\" (Em desenvolvimento)")
    parser.add_argument("--midnight", default=None, help="Aplica o efeito 'midnight' em um vídeo. Exemplo: --midnight \"video_superior.mp4 video_inferior.mp4\" (Em desenvolvimento)")
    args = parser.parse_args()
    if not args.download == None:
        video = YoutubeVideo(args.download)

        if not args.output == None:
            video.save(path=args.output)
        else:
            video.save()
        return 

    if not args.file == None:
        if not args.cut == None:
            editor = MoviePyEditor(args.file)
            cut_params = dict(param.split('=') for param in args.cut.split())
            editor.cut(start=cut_params.get("start"), end=cut_params.get("end"))
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            output_path = args.output if not args.output == None else "video_cut.mp4"
            editor.save(path=output_path)
            return

        if not args.auto_legend == False:
            logger.info("Iniciando processo de geração de legendas automáticas...")
            speech = Speech(href=args.file)
            segments = speech.segments()
            editor = MoviePyEditor(args.file)
            logger.info(f"Gerando legendas para {len(segments)} segmentos de áudio...")
            for segment in segments:
                logger.debug(f"Adicionando segmento |Start: {segment.start}, End: {segment.end}, Text: {segment.text}|")
                editor.add_legend(start=segment.start, end=segment.end, text=segment.text)
            logger.info("Legendas geradas, salvando vídeo com legendas...")
            output_path = args.output if not args.output == None else "video_with_legends.mp4"
            editor.save(path=output_path)
            speech.close()
            editor.close()
            return
        return
    if args.effect == True:
        logger.info("Modo de edição interativa selecionado.")
        if args.join is not None: # avtools --effect --join "um/video2.mp4 um/video1.mp4" -o video_joined.mp4
            logger.info(f"Concatenando vídeos: {args.join}")
            concat_videos = args.join.split(" ")
            videos = []
            for video in concat_videos[1:]:
                videos.append(VideoFileClip(video))
            logger.info(f"Salvando vídeo concatenado em {args.output}...")
            strategy = MontConcatStrategy(video_paths=concat_videos)
            strategy.save(args.output)
            logger.info("Vídeo com efeito 'concatenado' salvo com sucesso.")
            strategy.close()
        elif args.midnight is not None: # avtools --effect --midnight "um/video2.mp4 um/video1.mp4" -o video_midnight.mp4
            logger.info(f"Aplicando efeito 'midnight' nos vídeos: {args.midnight}")
            paths = args.midnight.split(" ")
            video_superior = VideoFileClip(paths[0])
            video_inferior = VideoFileClip(paths[1])
            videos = [video_superior, video_inferior]
            strategy = MontMidnightStrategy(video_paths=videos)
            logger.info(f"Salvando vídeo com efeito 'midnight' em {args.output}...")
            strategy.save(args.output)
            logger.info("Vídeo com efeito 'midnight' salvo com sucesso.")
            strategy.close()
        else:
            logger.warning("Nenhum vídeo para concatenar foi fornecido.")
            return
        

        

    parser.print_help()

    
    



    # video = YoutubeVideo(args.href)
    # pprint(asdict(video))
    # video.save()
    # speech = Speech(href=args.output)
    # result = speech.transcribe()
    # writer = open("transcript.txt", "w", encoding="utf-8")
    # writer.write(result["text"])
    # writer.close()


if __name__ == "__main__":
    main()