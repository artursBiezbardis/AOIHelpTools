import os


class FileAndFolderPathUtilities:

    @staticmethod
    def get_folder_path_from_file_path(file_path, level=1):
        folder = os.path.dirname(file_path)
        for file_path in range(level):
            folder = os.path.dirname(folder)
        return folder
