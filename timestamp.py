from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def gen_ass_timestamp(file):
    audio = AudioSegment.from_file(file)
    return detect_nonsilent(audio, silence_thresh=-46, min_silence_len=500)
