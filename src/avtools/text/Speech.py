from xml.parsers.expat import model
import whisper
import os

class Segment:
    def __init__(self, start, end, text):
        self.start = start
        self.end = end
        self.text = text

class Speech():
    def __init__(self, href="video.mp4"):
        self.result = None
        self.cached = None
        self.segment = None

        self.href = href
        if os.path.exists("cached.srt"):
            self.cached = open("cached.srt", "r", encoding="utf-8").read()

    def transcribe(self, model_name="turbo"):
        model =  whisper.load_model(model_name)
        segs = []
        if self.cached is not None:
            self.segment = segs
            lines = self.cached.strip().split('\n\n')
            for line in lines:
                if line.strip():
                    parts = line.split('\n', 2)
                    if len(parts) == 3:
                        start_end = parts[0].split(' --> ')
                        start, end = float(start_end[0]), float(start_end[1])
                        text = parts[2]
                        segs.append(Segment(start=start, end=end, text=text))
            return segs
        else:
            result = model.transcribe(self.href)
            writer = open("cached.srt", "w", encoding="utf-8")
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                writer.write(f"{start} --> {end}\n{text}\n\n")
            writer.close()
            for s in result["segments"]:
                segs.append(Segment(start=s["start"], end=s["end"], text=s["text"]))
            self.segment = segs
            return segs

    def segments(self):
        segs = []
        if self.segment == None:
            if self.cached is not None:
                lines = self.cached.strip().split('\n\n')
                for line in lines:
                    if line.strip():
                        parts = line.split('\n', 2)
                        if len(parts) == 2:
                            start_end = parts[0].split(' --> ')
                            start, end = float(start_end[0]), float(start_end[1])
                            text = parts[1]
                            segs.append(Segment(start=start, end=end, text=text))
                self.segment = segs
                return segs
            else:
                self.transcribe()
                return self.segment
        else:
            return self.segment

    def close(self):
        if os.path.exists("cached.srt"):
            os.remove("cached.srt")
