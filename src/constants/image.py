IMAGE_EXTENSIONS = {ext for base in [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"
] for ext in (base.lower(), base.upper())}
