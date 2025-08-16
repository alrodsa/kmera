from unittest import TestCase
from src.metadata.photo import PhotoMetadata


class TestPhotoMetadata(TestCase):
    def setUp(self):
        self.camera_model = "Canon EOS 5D Mark IV"
        self.exposure_time = "1/125"
        self.aperture = "27/10"
        self.iso = "100"
        self.focal_length = "50mm"
        self.date_taken = "2023-10-01"
        self.location = "New York, USA"
        self.description = "A beautiful day in the city."
        self.exposure_bias = "0"

    def test_photo_metadata_creation(self):
        metadata = PhotoMetadata(
            camera_model=self.camera_model,
            exposure_time=self.exposure_time,
            aperture=self.aperture,
            iso=self.iso,
            focal_length=self.focal_length,
            date_taken=self.date_taken,
            location=self.location,
            description=self.description,
            exposure_bias=self.exposure_bias
        )
        self.assertEqual(metadata.camera_model, self.camera_model)
        self.assertEqual(metadata.exposure_time, "1s125")
        self.assertEqual(metadata.aperture, "2.7f")
        self.assertEqual(metadata.iso, self.iso)
        self.assertEqual(metadata.focal_length, self.focal_length)
        self.assertEqual(metadata.date_taken, self.date_taken)
        self.assertEqual(metadata.location, self.location)
        self.assertEqual(metadata.description, self.description)
        self.assertEqual(metadata.exposure_bias, self.exposure_bias)

    def test_photo_metadata_str(self):
        metadata = PhotoMetadata(
            camera_model=self.camera_model,
            exposure_time=self.exposure_time,
            aperture=self.aperture,
            iso=self.iso,
            focal_length=self.focal_length,
            date_taken=self.date_taken,
            location=self.location,
            description=self.description,
            exposure_bias=self.exposure_bias
        )
        self.assertEqual(str(metadata), "1s125-2.7f-100")
