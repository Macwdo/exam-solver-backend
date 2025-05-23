import os


class StorageManager:
    def __init__(self) -> None:
        self._tracked_files = set()

    def track_file(self, file_path: str):
        self._tracked_files.add(file_path)

    def cleanup(self):
        for file_path in self._tracked_files:
            os.remove(file_path)

        self._tracked_files.clear()
