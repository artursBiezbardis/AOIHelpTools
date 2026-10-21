import os


class RecipesListRepository:

    @staticmethod
    def folder_dict(path):
        dirs = {}
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir():
                    dirs[entry.name] = entry.path
        return dirs



