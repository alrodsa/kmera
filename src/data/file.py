from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from src.metadata.photo import PhotoMetadata
import exifread
import piexif

@dataclass
class File:
    name: str
    size: int
    directory: str

    @cached_property
    def extension(self) -> str:
        return Path(self.name).suffix

    @cached_property
    def photo_metadata(self) -> PhotoMetadata:
        with open(Path(self.directory), 'rb') as f:
            tags = exifread.process_file(f)
            return PhotoMetadata(
                camera_model=str(tags.get("Image Model", "")).rstrip(),
                exposure_time=str(tags.get("EXIF ExposureTime", "")).rstrip(),
                aperture=str(tags.get("EXIF FNumber", "")).rstrip(),
                iso=str(tags.get("EXIF ISOSpeedRatings", "")).rstrip(),
                focal_length=str(tags.get("EXIF FocalLength", "")).rstrip(),
                date_taken=str(tags.get("EXIF DateTimeOriginal", "")).rstrip(),
                location=f"{tags.get('GPS GPSLatitude', '').rstrip()}{tags.get('GPS GPSLongitude', '').rstrip()}",
                description=str(tags.get("Image ImageDescription", "")).rstrip(),
                exposure_bias=str(tags.get("EXIF ExposureBiasValue", "")).rstrip()
            )

    @cached_property
    def exif_bytes(self) -> bytes:
        return piexif.dump(piexif.load(self.directory))

    def __str__(self) -> str:
        return (
            f"{Path(self.name).stem}_{str(self.photo_metadata)}{self.extension}"
        )
