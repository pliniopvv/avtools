import argparse
from dataclasses import asdict
from pprint import pprint

from .text import Speech
from .video import MoviePyEditor, YoutubeVideo

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main():
    parser = argparse.ArgumentParser(description="Canivete Suíço da edição vídeos em geral por linha de comandos.")
    
    parser.add_argument("-s", "--href", help="URL do vídeo a ser processado.")
    parser.add_argument("-F", "--file", help="Caminho do arquivo de vídeo a ser editado.")
    parser.add_argument("-al", "--auto-legend", action="store_true", help="Gera legendas automáticas para o vídeo.")
    parser.add_argument("-o", "--output", help="Caminho do arquivo de saída.")

    parser.add_argument("-v", "--version", action="version", version="avtools 0.1.0")

    parser.add_argument("--cut", help="Corta o vídeo de acordo com os parâmetros informados. Exemplo: --cut \"start=00:01:00 end=00:02:00\"")

    args = parser.parse_args()
    if not args.href == None:
        video = YoutubeVideo(args.href)

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
            editor.close()
            return

    args.print_help()

    
    



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