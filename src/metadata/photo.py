from pydantic import BaseModel

class PhotoMetadata(BaseModel):
    camera_model: str
    exposure_time: str
    aperture: str
    iso: str
    focal_length: str
    date_taken: str
    location: str
    description: str
