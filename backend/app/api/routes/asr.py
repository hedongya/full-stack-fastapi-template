from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.asr_service import transcribe_audio

router = APIRouter()


@router.post("/transcribe")
async def transcribe_endpoint(file: UploadFile = File(...)):
    """Transcribe audio file to text using ASR service"""
    try:
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        audio_content = await file.read()
        result = await transcribe_audio(audio_content)
        return {"text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
