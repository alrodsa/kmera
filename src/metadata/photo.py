from pydantic import BaseModel, field_validator

class PhotoMetadata(BaseModel):
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
