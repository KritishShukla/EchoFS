import os
from pathlib import Path
from apps.common.constants.workspace import WORKSPACE_DIR

class FileService:
    @staticmethod
    def _validate_path(file_path):
        full_path = WORKSPACE_DIR / file_path
        if not str(full_path).startswith(str(WORKSPACE_DIR)):
            raise ValueError("Path outside workspace not allowed")
        return full_path
    
    @staticmethod
    def create_file(file_path, content):
        full_path = FileService._validate_path(file_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        return f"File created: {file_path}"
    
    @staticmethod
    def read_file(file_path):
        full_path = FileService._validate_path(file_path)
        if not full_path.exists():
            return f"File not found: {file_path}"
        return full_path.read_text()
    
    @staticmethod
    def list_files(directory_path=""):
        full_path = FileService._validate_path(directory_path)
        if not full_path.exists():
            return f"Directory not found: {directory_path}"
        files = [str(p.relative_to(WORKSPACE_DIR)) for p in full_path.rglob("*") if p.is_file()]
        return "\n".join(files) if files else "No files found"
    
    @staticmethod
    def delete_file(file_path):
        full_path = FileService._validate_path(file_path)
        if not full_path.exists():
            return f"File not found: {file_path}"
        full_path.unlink()
        return f"File deleted: {file_path}"