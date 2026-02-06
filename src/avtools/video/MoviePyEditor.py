from moviepy.editor import VideoFileClip

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MoviePyEditor():
    def __init__(self, href: str) -> None:
        self.href = href
        self.clip = VideoFileClip(href)
        self.legends = []

    def cut(self, start: str, end: str):
        start_seconds = start
        end_seconds = end
        self.clip = self.clip.subclip(start_seconds, end_seconds)

    def add_legend(self, start: str, end: str, text: str):
        # fontsize=100,color='yellow',stroke_color='black', stroke_width=2, font='Bangers-Regular.ttf'
        self.legends.append({
            "start": start,
            "end": end,
            "text": text
        })

    def save(self, path: str):
        logger.info(f"Salvando vídeo em {path}...")
        if len(self.legends) > 0:
            from moviepy.editor import TextClip, CompositeVideoClip
            txt_clips = []
            for legend in self.legends:
                logger.debug(f"Adicionando legenda: {legend}")
                txt_clip = TextClip(legend["text"], fontsize=100,color='yellow',stroke_color='black', stroke_width=2, font='src/assets/Bangers-Regular.ttf', size=(self.clip.w * 0.8, None), method='caption')
                txt_clip = txt_clip.set_position(("center","bottom")).set_duration(float(legend["end"]) - float(legend["start"])).set_start(float(legend["start"]))
                txt_clips.append(txt_clip)
            logger.info(f"Combinando clipes de texto com o vídeo principal...")
            self.clip = CompositeVideoClip([self.clip, *txt_clips])

        try:
            logger.info("Iniciando escrita do arquivo de vídeo...")
            self.clip.write_videofile(path)
            logger.info("Vídeo salvo com sucesso.")
        finally:
            try:
                self.clip.close()
            except Exception:
                logger.debug("Erro ao fechar o clipe de vídeo após salvar.", exc_info=True)
                pass

    def close(self):
        try:
            if hasattr(self, 'clip') and self.clip is not None:
                self.clip.close()
        except Exception:
            pass