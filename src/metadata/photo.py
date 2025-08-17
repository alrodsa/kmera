from pydantic import BaseModel, field_validator

class PhotoMetadata(BaseModel):
    """
    A class representing metadata for a photo.

    Attributes
    ----------
    camera_model : str
        The model of the camera used to take the photo.
    exposure_time : str
        The exposure time of the photo.
    aperture : str
        The aperture setting of the camera when the photo was taken.
    iso : str
        The ISO speed rating of the camera when the photo was taken.
    focal_length : str
        The focal length of the lens used to take the photo.
    date_taken : str
        The date and time when the photo was taken.
    location : str
        The GPS coordinates of the location where the photo was taken.
    description : str
        A description of the photo.
    exposure_bias : str
        The exposure bias setting of the camera when the photo was taken.
    """
    
    camera_model: str
    exposure_time: str
    aperture: str
    iso: str
    focal_length: str
    date_taken: str
    location: str
    description: str
    exposure_bias: str

    @field_validator("exposure_time", mode="before")
    @classmethod
    def validate_exposure_time(cls, value):
        return value.replace('/', 's')

    @field_validator("aperture",mode="before")
    @classmethod
    def validate_aperture(cls, value):
        if '/' in value:
            aperture_parts = value.split('/')
            if len(aperture_parts) == 2:
                return str(
                    round(float(aperture_parts[0]) / float(aperture_parts[1]), 1)
                ) + 'f'
        return value + 'f'

    def __str__(self) -> str:
        return (
            f"{self.exposure_time}-{self.aperture}-{self.iso}"
        )
