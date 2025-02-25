import logging
import os
import uuid

import uvicorn
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database import SessionLocal, Image, ImageMetadata

log = logging.getLogger(__name__)

app = FastAPI()

UPLOAD_DIR = "bucket"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ROOT_API = "/api"
ROOT_IMAGES = f"{ROOT_API}/images"


@app.post("%s" % ROOT_IMAGES)
async def upload_image(file: UploadFile = File(...),
                       db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, str(uuid.uuid4()))
    # Save metadata to DB
    image = Image(location=file_path, origin_filename=file.filename)
    db.add(image)
    db.commit()
    db.refresh(image)
    img_id = image.id

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    resource_uri = f"%s/{img_id}" % ROOT_IMAGES
    return JSONResponse(content={"id": img_id, "resource_uri": resource_uri},
                        status_code=201)


@app.put("%s/{img_id}" % ROOT_IMAGES)
async def update_image(img_id: int, metadata: ImageMetadata, db: Session = Depends(get_db)):
    img = await get_img_or_404(img_id, db)
    img.business_code = metadata.business_code
    img.description = metadata.description
    db.commit()
    db.refresh(img)
    return JSONResponse(content=img.to_dict(), status_code=200)


# Retrieve Image
@app.get("%s/{img_id}" % ROOT_IMAGES)
async def get_image(img_id: int, db: Session = Depends(get_db)):
    img = await get_img_or_404(img_id, db)

    def file_stream():
        with open(img.location, "rb") as f:
            yield from f

    headers = {
        "Content-Disposition": f'attachment; filename="{img.origin_filename}"'
    }

    return StreamingResponse(file_stream(), media_type="image/jpeg", headers=headers)


@app.get("%s" % ROOT_IMAGES)
async def get_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()
    return list(map(lambda x: x.to_dict(), images))


@app.get("%s/{img_id}/metadata" % ROOT_IMAGES)
async def get_image_metadata(img_id: int, db: Session = Depends(get_db)):
    img = await get_img_or_404(img_id, db)
    return JSONResponse(content=img.to_dict(), status_code=200)


async def get_img_or_404(img_id, db):
    img = db.query(Image).filter(Image.id == img_id).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return img


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
