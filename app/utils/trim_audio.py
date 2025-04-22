import base64
import io
from io import BytesIO

from flask import current_app
from pydub import AudioSegment, exceptions as pydub_exc

def _trim_15_seconds(raw: bytes) -> bytes:
    from pydub import AudioSegment, exceptions

    audio = AudioSegment.from_file(io.BytesIO(raw))   # <-- fallaba sin ffmpeg
    clip  = audio[:15_000]                            # primeros 15 s

    out   = io.BytesIO()
    clip.export(out, format="mp3", bitrate="128k")
    return out.getvalue()                             # <-- bytes reales

