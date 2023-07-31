import os


class RecipesListRepository:

    def folder_dict(self, path):
        dirs = {}
        for name in os.listdir(path):
            if os.path.isdir(os.path.join(path, name)):
                dirs[name] = os.path.join(path, name)
        return dirs



