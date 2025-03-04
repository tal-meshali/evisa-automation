from enum import Enum


class UploadStatus(Enum):
    Empty = 0
    Invalid = 1
    Uploaded = 2
    Valid = 3
