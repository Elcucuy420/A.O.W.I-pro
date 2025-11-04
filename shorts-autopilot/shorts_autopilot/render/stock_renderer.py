import os, random
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip

# Very light stock stitcher: picks clips from assets/stock and overlays text.
# Drop your vertical stock into assets/stock/*.mp4

def render_with_stock(script, voice_path, out_path='output.mp4'):
    assets_dir='assets/stock'
    clips=[os.path.join(assets_dir,f) for f in os.listdir(assets_dir) if f.endswith('.mp4')] if os.path.isdir(assets_dir) else []
    if not clips:
        from .simple_renderer import render
        return render(script, voice_path, out_path=out_path, duration=35)
    pick = random.choice(clips)
    base = VideoFileClip(pick).resize(height=1920)
    txt_lines=[script['hook']] + script.get('body',[]) + [script.get('cta','')]; text='
'.join([l for l in txt_lines if l])
    tc=TextClip(text, fontsize=60, method='caption', size=(base.w-100, base.h-300)).set_duration(min(base.duration,35)).set_position('center')
    ac=AudioFileClip(voice_path) if voice_path else None
    dur=min(base.duration, ac.duration if ac else 35)
    comp=CompositeVideoClip([base.set_duration(dur), tc]).set_audio(ac).set_duration(dur)
    comp.write_videofile(out_path, fps=30, codec='libx264', audio_codec='aac')
    return out_path
