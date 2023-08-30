from typing import Union
import base64
from typing import Annotated

from fastapi import FastAPI, Form
from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from pydub import AudioSegment
from pydub.playback import play
import torch
app = FastAPI()


print(torch.cuda.is_available())
# download and load all models
preload_models()
print("model loaded")
# text_prompt = """
# Hello, my name is Nose. And uh, and I like hamburger. Hahaha... But I also have other interests such as playing tactic toast.
# """
# audio_array = generate_audio(text_prompt)
#
# # save audio to disk
# write_wav("vallex_generation.wav", SAMPLE_RATE, audio_array)

# song = AudioSegment.from_wav("vallex_generation.wav")
# play(song)


@app.post("/read/")
async def login(txt: Annotated[str, Form()],voiceman: Annotated[str, Form()],lang: Annotated[str, Form()]):
    print("{}|{}|{}".format(voiceman,txt,lang))
    # if lang=="jp":
    #     txt="[JP]"+txt+"[JP]"
    # elif lang=="en":
    #     txt="[EN]"+txt+"[EN]"
    print(txt)
    audio_array = generate_audio(txt)

    # save audio to disk
    write_wav("vallex_generation.wav", SAMPLE_RATE, audio_array)
    AudioSegment.from_wav("./vallex_generation.wav").export("./vallex_generation.mp3", format="mp3")
    in_file = open("vallex_generation.mp3", "rb")  # opening for [r]eading as [b]inary
    data = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()

    return base64.b64encode(data)