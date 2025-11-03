# Shorts Autopilot (V1) — Evolving Niche AI Channels

**Goal:** Fully autonomous YouTube Shorts/TikTok pipeline that *self-evolves the niche* using performance signals.

### Features
- Topic discovery via trend scouts (news + Reddit + YouTube search).
- Scriptwriter (concise 15–35s hooks) with A/B variants.
- Voiceover via ElevenLabs or local TTS fallback.
- Footage builder: stock b-roll, memes, captions, SRT subtitles.
- Auto-upload to YouTube + TikTok with tags, SEO title, description.
- Comment auto-replies for first 60 minutes after publish.
- **Niche evolution engine**: shifts content based on rolling 7/30-day CTR, retention, RPM, and follower growth.

### Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp shorts-autopilot/.env.example .env
python -m shorts_autopilot.cli bootstrap
```

### Safety & Policy
- No scraping of private data.
- Respect platform TOS.
- Human-in-the-loop override supported via `/control/decisions.json`.
