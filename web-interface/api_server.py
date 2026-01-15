from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Setup
project_root = Path(__file__).parent
load_dotenv(project_root / '.env')
sys.path.append(str(project_root / 'scripts'))

app = FastAPI()

# Input Models
class StoryInput(BaseModel):
    id: str
    theme: str
    name: str
    base_text: Optional[str] = None

class ScriptEdit(BaseModel):
    id: str
    content: str

# Endpoints
@app.get("/health")
def health_check():
    return {"status": "ok", "mode": "local_studio"}

@app.post("/generate/script")
def generate_script(data: StoryInput):
    """Chama o script de geração de roteiro"""
    # ... wrapper para generate_custom.py ...
    return {"status": "mock", "content": "Roteiro gerado aqui..."}

@app.get("/assets/{story_id}")
def get_assets(story_id: str):
    """Lista imagens e áudio já gerados"""
    output_dir = project_root / 'output'
    images = list((output_dir / 'images_unsplash').glob(f"scene_*"))
    return {
        "images": [img.name for img in images],
        "audio_exists": (output_dir / 'audio' / f'audio_{story_id}.mp3').exists()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
