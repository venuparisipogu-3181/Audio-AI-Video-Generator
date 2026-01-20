import gradio as gr
import os
import asyncio
from video_generator import generate_telugu_video

os.makedirs("temp", exist_ok=True)
os.makedirs("output", exist_ok=True)

def create_video(idea, style, voice):
    if not idea.strip():
        return "ఐడియా ఇవ్వండి!", None
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        status, video_path = loop.run_until_complete(
            generate_telugu_video(idea, style, voice)
        )
        loop.close()
        return status, video_path if video_path and os.path.exists(video_path) else None
    except Exception as e:
        return f"సమస్య: {str(e)}", None

with gr.Blocks(title="తెలుగు AI వీడియో", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎬 **తెలుగు AI వీడియో స్టూడియో** 
    **FREE • 100% తెలుగు డైలాగ్స్ • Professional**
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            idea_input = gr.Textbox(
                label="💡 మీ ఐడియా", 
                placeholder="గ్రామ దెయ్యం, ప్రేమ కథ, మోటివేషన్...", 
                lines=3
            )
            
            style_input = gr.Dropdown(
                choices=["కార్టూన్", "3D", "అనిమే", "సినిమాటిక్"],
                value="కార్టూన్",
                label="🎨 స్టైల్"
            )
            
            voice_input = gr.Dropdown(
                choices=["మోహన్", "శ్రుతి", "పిల్లాడు", "అమ్మాయి", "తాత"],
                value="మోహన్",
                label="🎙️ వాయిస్"
            )
            
            generate_btn = gr.Button("🚀 వీడియో క్రియేట్", variant="primary", size="lg")
        
        with gr.Column(scale=2):
            status_output = gr.Textbox(label="📊 ప్రోగ్రెస్", lines=12)
            video_output = gr.Video(label="🎥 తెలుగు వీడియో")
    
    generate_btn.click(create_video, [idea_input, style_input, voice_input], [status_output, video_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
