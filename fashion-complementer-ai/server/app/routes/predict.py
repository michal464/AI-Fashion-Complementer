from fastapi import APIRouter, UploadFile, File, HTTPException
from app.controllers.predict_controller import predict_from_bytes
from app.database import history_collection
from datetime import datetime

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="יש להעלות קובץ תמונה בלבד.")

    image_bytes = await file.read()
    result = predict_from_bytes(image_bytes)

    history_collection.insert_one({
        "filename": file.filename,
        "style": result["style"],
        "confidence": result["confidence"],
        "timestamp": datetime.utcnow(),
    })

    return result
