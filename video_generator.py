import os
import asyncio
import edge_tts
from moviepy.editor import *
from PIL import Image
import google.generativeai as genai

# CHANGE THIS: Your FREE Gemini API key
GEMINI_API_KEY = "AIzaSyD_-TVRqARqdETRzylX_bynWkZCVtsPF-A"  
genai.configure(AIzaSyDYf7vOBgmogqZsfJrzGPEL4np62BHsGrk)

# Telugu dialogues ONLY (100% guarantee)
TELUGU_DIALOGUES = {
    "horror": [
        "అమ్మో! అక్కడ ఏదో కనిపిస్తోంది!",
        "అది దెయ్యం! పరిగెత్తాలి!",
        "అమ్మా! నా కోసం వచ్చారా?"
    ],
    "love": [
        "నీలోనే నా ప్రపంచం కనిపిస్తుంది",
        "నీ చూపుల్లో మాయా మళ్లీ",
        "మనం ఎప్పటికీ కలిసి ఉండాలి"
    ],
    "motivation": [
        "నమస్కారం స్నేహితులారా!",
        "విజయం కోసం కష్టపడాలి",
        "మీరు అసాధారణమైనవారు!"
    ]
}

VOICE_MAP = {
    "మోహన్": "te-IN-MohanNeural",
    "శ్రుతి": "te-IN-ShrutiNeural", 
    "పిల్లాడు": "te-IN-ShrutiNeural",
    "అమ్మాయి": "te-IN-ShrutiNeural",
    "తాత": "te-IN-MohanNeural"
}

async def generate_telugu_video(idea, style, voice_style):
    status_lines = ["🚀 Video generation started..."]
    
    # Select Telugu scenes
    scenes = TELUGU_DIALOGUES["motivation"]
    status_lines.append(f"✅ {len(scenes)} Telugu scenes loaded")
    
    clip_paths = []
    
    # Process each scene
    for i, dialogue in enumerate(scenes):
        clip_path = f"temp/scene_{i:03d}.mp4"
        
        # Skip if exists (resume feature)
        if os.path.exists(clip_path):
            status_lines.append(f"⏭️ Scene {i+1} already exists")
            clip_paths.append(clip_path)
            continue
        
        status_lines.append(f"🎬 Processing scene {i+1}: {dialogue[:20]}...")
        
        try:
            # Step 1: Telugu voice generation
            voice_path = f"temp/voice_{i}.mp3"
            voice_code = VOICE_MAP.get(voice_style, "te-IN-MohanNeural")
            
            communicate = edge_tts.Communicate(dialogue, voice_code)
            await communicate.save(voice_path)
            
            # Step 2: Colorful background
            colors = [(100,150,200),(200,100,150),(150,200,100),(255,150,100)]
            img = Image.new('RGB', (1280, 720), color=colors[i%4])
            img_path = f"temp/bg_{i}.png"
            img.save(img_path)
            
            # Step 3: Video with zoom effect
            audio_clip = AudioFileClip(voice_path)
            img_clip = ImageClip(img_path, duration=audio_clip.duration)
            
            # Smooth zoom animation
            zoomed = img_clip.resize(lambda t: 1 + 0.2*(t/audio_clip.duration))
            final_scene = zoomed.set_audio(audio_clip)
            
            # Export scene
            final_scene.write_videofile(
                clip_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            clip_paths.append(clip_path)
            
            # Memory cleanup
            audio_clip.close()
            img_clip.close()
            final_scene.close()
            
        except Exception as e:
            status_lines.append(f"⚠️ Scene {i+1} failed: {str(e)}")
            continue
    
    # Combine scenes
    if clip_paths:
        status_lines.append("🎞️ Combining all scenes...")
        
        final_clips = [VideoFileClip(p) for p in clip_paths]
        final_video = concatenate_videoclips(final_clips)
        
        output_path = "output/telugu_video.mp4"
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        final_video.close()
        for clip in final_clips: clip.close()
        
        status_lines.append("🎉 Telugu AI video ready!")
        return "\n".join(status_lines), output_path
    
    return "❌ No clips generated", None
