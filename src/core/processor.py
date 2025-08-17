from pathlib import Path
import shutil
from tqdm import tqdm
from src.data.file import File
from src.data.folder import Folder
import cv2
from PIL import Image

class Processor:
    """
    A class to process folders and files, copying or replacing metadata
    in images and organizing files based on their metadata.
    """

    @staticmethod
    def copy_naming_metadata(
        folder: Folder, source_root: Path, output_root: Path, in_image: bool
    ) -> "Processor":
        """
        Copy files from the source folder to the output folder, preserving the
        directory structure. If `in_image` is True, it adds metadata inside the image.

        Parameters
        ----------
        folder : Folder
            The folder object containing files and subfolders to be processed.
        source_root : Path
            The root path of the source directory.
        output_root : Path
            The root path of the output directory where files will be copied.
        in_image : bool
            If True, adds metadata inside the image files.

        Returns
        -------
        Processor
            The Processor instance for method chaining.
        """

        relative_path = Path(folder.directory).relative_to(source_root)
        dest_dir = output_root / relative_path
        dest_dir.mkdir(parents=True, exist_ok=True)

        for file in tqdm(
            folder.files,
            desc=f"📂 Copying files from {folder.directory}",
            unit="file",
            leave=False,
            bar_format="{l_bar}💾|{bar:30}📸| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
            colour="green"
        ):
            src_file = Path(file.directory)
            dst_file = dest_dir / str(file)

            if in_image:
                Processor.add_metadata_inside_image(file, str(dst_file))
                continue

            shutil.copy2(src_file, dst_file)

        for subfolder in tqdm(
            folder.folders,
            desc=f"📂 Copying subfolders from {folder.directory}",
            unit="folder",
            leave=False,
            bar_format="{l_bar}💾|{bar:30}📸| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
            colour="blue"
        ):
            Processor.copy_naming_metadata(subfolder, source_root, output_root, in_image)

    @staticmethod
    def replace_naming_metadata(folder: Folder, in_image: bool) -> "Processor":
        """
        Replace files in the folder with their metadata information.
        This method renames files based on their metadata and moves them to their
        respective directories.

        Parameters
        ----------
        folder : Folder
            The folder object containing files and subfolders to be processed.
        in_image : bool
            If True, adds metadata inside the image files.

        Returns
        -------
        Processor
            The Processor instance for method chaining.
        """
        for file in tqdm(
            folder.files,
            desc=f" ✍️ Replacing files in {folder.directory}",
            unit="file",
            leave=False,
            bar_format="{l_bar}💾|{bar:30}📸| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
            colour="green"
        ):
            if in_image:
                Processor.add_metadata_inside_image(file, file.directory)

            shutil.move(Path(file.directory), Path(file.directory).with_name(str(file)))

        for subfolder in tqdm(
            folder.folders,
            desc=f" ✍️ Replacing subfolders in {folder.directory}",
            unit="folder",
            leave=False,
            bar_format="{l_bar}💾|{bar:30}📸| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
            colour="blue"
        ):
            Processor.replace_naming_metadata(subfolder, in_image)

    @staticmethod
    def add_metadata_inside_image(file: File, dst_file: str) -> "Processor":
        """
        Open the image file with OpenCV and add photo metadata inside it
        with a semi-transparent background and white text. The metadata
        includes exposure time, aperture, ISO and EV (exposure bias).

        Parameters
        ----------
        file : File
            The file object containing the image and its metadata.
        dst_file : str
            The destination file path where the modified image will be saved.

        Returns
        -------
        Processor
            The Processor instance for method chaining.
        """
        image = cv2.imread(file.directory)
        if image is None:
            print(f"Error: Could not read image {file.directory}, skipping...")
            return

        _, w, _ = image.shape

        metadata = file.photo_metadata
        lines = [
            f"Exposure: {metadata.exposure_time.replace('s', '/')}",
            f"Aperture: {metadata.aperture}",
            f"ISO: {metadata.iso}",
            f"EV: {metadata.exposure_bias}"
        ]

        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = max(0.8, w / 1000)
        thickness = max(2, w // 800)
        line_height = int(40 * font_scale)
        padding_internal = int(15 * font_scale)
        padding_external = int(30 * font_scale)

        sizes = [cv2.getTextSize(line, font, font_scale, thickness)[0] for line in lines]
        text_width = max(size[0] for size in sizes)
        text_height = len(lines) * line_height

        x, y = padding_external, padding_external + sizes[0][1]
        top_left_x = x - padding_internal
        top_left_y = y - sizes[0][1] - padding_internal
        bottom_right_x = x + text_width + padding_internal
        bottom_right_y = y + text_height - (line_height - sizes[0][1]) + padding_internal

        overlay = image.copy()
        cv2.rectangle(overlay, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, image, 0.5, 0, image)

        border_thickness = max(3, int((4 * font_scale)/2))
        cv2.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (255, 255, 255), border_thickness)

        for i, line in enumerate(lines):
            line_y = y + i * line_height
            cv2.putText(image, line, (x, line_y), font, font_scale, (255, 255, 255), thickness)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)

        pil_image.save(dst_file, "jpeg", exif=file.exif_bytes)
