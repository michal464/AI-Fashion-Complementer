import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pymongo.collection import Collection

from app.database import get_items_collection
from app.controllers.recommend_controller import get_recommendations

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/recommend")
async def recommend(
    file: UploadFile = File(...),
    collection: Collection = Depends(get_items_collection),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Image file required.")

    try:
        image_bytes = await file.read()
        result = get_recommendations(image_bytes, collection)
        return result
    except Exception as e:
        logger.exception("Recommendation failed")
        raise HTTPException(status_code=500, detail=str(e))
