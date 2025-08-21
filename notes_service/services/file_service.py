"""File Service Module"""

import os
from fastapi import UploadFile
from notes_service.config.logging import logger
from notes_service.config.settings import AppConfig
from notes_service.errors.notes_errors import NotesException


class FileService:
    """File Service Class"""

    def __init__(self, upload_dir: str, app_config: AppConfig) -> None:
        self.upload_dir = upload_dir
        self.app_config = app_config

    async def save_file(self, file: UploadFile) -> str:
        """
        Save an uploaded file to the local filesystem.

        Args:
            file (UploadFile): File object from FastAPI.

        Returns:
            str: Path where file was saved.
        """
        try:
            logger.info("Saving file: %s", file.filename)
            file_path = os.path.join(self.upload_dir, file.filename)
            # Write the file to disk
            with open(file_path, "wb") as f:
                contents = await file.read()
                f.write(contents)
            logger.info("File saved successfully: %s", file_path)
            return file_path
        except Exception as e:
            logger.error("Error saving file: %s", str(e))
            raise NotesException(
                f"Failed to save file {file.filename}: {str(e)}",
                status_code=500,
                details=str(e),
            )

    def delete_file(self, file_path: str) -> bool:
        """Delete file from local folder by filename"""
        logger.info("Deleting file: %s", file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("File deleted successfully: %s", file_path)
            return True
        logger.warning("File not found: %s", file_path)
        return False
