import gradio as gr
import requests

COLAB_API_URL = "PASTE_YOUR_COLAB_WEBHOOK_URL_HERE"

def generate_video(topic, style, duration):
    payload = {
        "topic": topic,
        "style": style,
        "duration": duration
    }
    r = requests.post(COLAB_API_URL, json=payload)
    if r.status_code == 200:
        return r.json()["video_url"]
    return "Error: GPU worker not responding"

with gr.Blocks() as demo:
    gr.Markdown("## 🎬 AI Video Generator (n8n Style)")

    topic = gr.Textbox(label="విషయం / Topic")
    style = gr.Dropdown(
        ["Cinematic", "Anime", "Bible Story", "Motivational"],
        label="Style"
    )
    duration = gr.Slider(10, 60, value=30, label="Duration (seconds)")

    output = gr.Textbox(label="Final Video URL")

    btn = gr.Button("Generate Video")

    btn.click(
        generate_video,
        inputs=[topic, style, duration],
        outputs=output
    )

demo.launch()
