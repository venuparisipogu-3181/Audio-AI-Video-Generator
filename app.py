import gradio as gr
import torch
from diffusers import StableDiffusionPipeline
from TTS.api import TTS
from transformers import MusicGenForConditionalGeneration, MusicGenProcessor
from pydub import AudioSegment
import subprocess
import os

os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/audio", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# ---------------- IMAGE ----------------
def generate_image(prompt):
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    ).to("cuda")

    image = pipe(prompt).images[0]
    image.save("assets/images/scene.png")
    return "Image Generated"

# ---------------- TTS ----------------
def generate_voice(text):
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
    tts.tts_to_file(text=text, file_path="assets/audio/voice.wav")
    return "Voice Generated"

# ---------------- MUSIC ----------------
def generate_music():
    processor = MusicGenProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicGenForConditionalGeneration.from_pretrained(
        "facebook/musicgen-small"
    ).to("cuda")

    inputs = processor(
        ["cinematic background music"],
        sampling_rate=32000,
        return_tensors="pt"
    ).to("cuda")

    audio = model.generate(**inputs)
    processor.save_audio(audio[0], "assets/audio/music.wav")
    return "Music Generated"

# ---------------- MIX AUDIO ----------------
def mix_audio():
    voice = AudioSegment.from_file("assets/audio/voice.wav")
    music = AudioSegment.from_file("assets/audio/music.wav").apply_gain(-12)
    final = voice.overlay(music[:len(voice)])
    final.export("outputs/final.wav", format="wav")
    return "Audio Mixed"

# ---------------- VIDEO ----------------
def render_video():
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", "assets/images/scene.png",
        "-i", "outputs/final.wav",
        "-c:v", "libx264",
        "-t", "10",
        "-pix_fmt", "yuv420p",
        "outputs/final.mp4"
    ])
    return "Video Ready"

# ---------------- PIPELINE ----------------
def generate_video(idea):
    generate_image(idea)
    generate_voice(idea)
    generate_music()
    mix_audio()
    render_video()
    return "outputs/final.mp4"

# ---------------- UI ----------------
ui = gr.Interface(
    fn=generate_video,
    inputs=gr.Textbox(label="Idea / Prompt"),
    outputs=gr.Video(label="Generated Video"),
    title="AI Video Generator (Free HF GPU)",
    description="Idea → Image → Voice → Music → Video"
)

ui.launch()
