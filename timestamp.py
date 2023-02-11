from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from datetime import datetime


def gen_ass_timestamp(file):
    audio = AudioSegment.from_file(file)
    stamps = detect_nonsilent(audio, silence_thresh=-46, min_silence_len=200)
    ass = ("\n"
           "[V4+ Styles]\n"
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
           "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n"
           "\n"
           "[Events]\n"
           "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    for stamp in stamps:
        start = datetime.utcfromtimestamp(stamp[0] / 1000 - 0.05)
        end = datetime.utcfromtimestamp(stamp[1] / 1000 + 0.05)
        ass += f'Dialogue: 0,{start.strftime("%H:%M:%S.%f")},{end.strftime("%H:%M:%S.%f")},Default,,0,0,0,,\n'

    with open(f'{file.split(".")[0] + ".ass"}', 'w') as f:
        f.write(ass)


if __name__ == '__main__':
    file = '/Users/dax/Downloads/01月18日 午前９時のNHKニュース.mp3'
    gen_ass_timestamp(file)
