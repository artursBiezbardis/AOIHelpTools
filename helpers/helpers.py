import os


class Helpers:

    def get_filename_from_path(self, location):
        return os.path.basename(location)

    def replace_special_letters(self, input_string: str):
        # Dictionary mapping Latvian special characters to regular characters
        replacements = {
            'ā': 'a',
            'ē': 'e',
            'ī': 'i',
            'ū': 'u',
            'Ā': 'A',
            'Ē': 'E',
            'Ī': 'I',
            'Ū': 'U',
            'č': 'c',
            'ģ': 'g',
            'ķ': 'k',
            'ļ': 'l',
            'ņ': 'n',
            'š': 's',
            'ž': 'z',
            'Č': 'C',
            'Ģ': 'G',
            'Ķ': 'K',
            'Ļ': 'L',
            'Ņ': 'N',
            'Š': 'S',
            'Ž': 'Z'
        }

        for original, replacement in replacements.items():
            input_string = input_string.replace(original, replacement)

        return input_string

    def is_number(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def correct_path_string(self, path: str) -> str:
        return path.replace('/', '\\')

    @staticmethod
    def get_files_in_folder(folder_path: str) -> list:
        return os.listdir(folder_path)

    @staticmethod
    def has_extension(file_path, extension):
        _, file_extension = os.path.splitext(file_path)
        return file_extension == extension

    @staticmethod
    def level_down_path(path: str, level: int) -> str:
        path_list = path.split('/')
        for _ in range(level):
            path_list = path_list[:-1]

        delimiter = '/'
        return delimiter.join(path_list)

    @staticmethod
    def edit_hex_in_file(file_path, position, new_bytes):
        with open(file_path, 'r+b') as file:
            file.seek(position)  # Move to the desired position
            file.write(bytes.fromhex(new_bytes))  # Write the new hex data