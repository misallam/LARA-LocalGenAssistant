from typing import Iterator
import subprocess
import elevenlabs
import os
import json

from dotenv import load_dotenv

load_dotenv()

MPV_LOCATION = os.getenv("MPV_LOCATION")

elevenlabs.set_api_key(os.getenv('ELEVEN_LAPS_KEY'))

def get_audio_stream(llm):
    audio_stream = elevenlabs.generate(text=llm,
                                       voice='Alice',
                                       model="eleven_multilingual_v2",
                                       stream=True)
    for chunck in audio_stream:
        if chunck:
            yield chunck


def stream(audio_stream: Iterator[bytes]) -> bytes:
    mpv_command = [MPV_LOCATION,
                   "--no-cache", "--no-terminal", "--", "fd://0"]
    mpv_process = subprocess.Popen(
        mpv_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    audio = b""

    for chunk in audio_stream:
        if chunk is not None:
            mpv_process.stdin.write(chunk)
            mpv_process.stdin.flush()
            audio += chunk

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()

    return audio

async def astream(audio_stream: Iterator[bytes]) -> bytes:
    mpv_command = [MPV_LOCATION,
                   "--no-cache", "--no-terminal", "--", "fd://0"]
    mpv_process = subprocess.Popen(
        mpv_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    audio = b""

    async for chunk in audio_stream:
        if chunk is not None:
            mpv_process.stdin.write(chunk)
            mpv_process.stdin.flush()
            audio += chunk

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()

    return audio


async def astream_with_text(audio_stream: Iterator[bytes]) -> bytes:
    mpv_command = [MPV_LOCATION,
                   "--no-cache", "--no-terminal", "--", "fd://0"]
    mpv_process = subprocess.Popen(
        mpv_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    async for chunk in audio_stream:
        if chunk:
            if type(chunk) == str:
                        print(chunk, end="")
            else:
                mpv_process.stdin.write(chunk)
                mpv_process.stdin.flush()

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()
