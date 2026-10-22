import os

# Letters that can appear in values float() accepts (nan, inf, infinity, exponents).
_FLOAT_LETTERS = frozenset('eEnNaAiIfFtTyY')


def _has_disallowed_letter(text: str) -> bool:
    for char in text:
        if char.isalpha() and char not in _FLOAT_LETTERS:
            return True
    return False


class Helpers:
    # Built once. These letters are outside Latin-1, where str.translate is slower
    # than a direct replace, and most mash cells contain none of them.
    _LATVIAN_TO_ASCII = {
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
        'Ž': 'Z',
    }

    def get_filename_from_path(self, location):
        return os.path.basename(location)

    def replace_special_letters(self, input_string: str):
        for original, replacement in self._LATVIAN_TO_ASCII.items():
            if original in input_string:
                input_string = input_string.replace(original, replacement)
        return input_string

    def try_float(self, string):
        """Return float(string), or None when it is not a float.

        float('nan') is returned as NaN, not None. TypeError still propagates.
        """
        if isinstance(string, str) and _has_disallowed_letter(string):
            return None
        try:
            return float(string)
        except ValueError:
            return None

    def is_number(self, string):
        return self.try_float(string) is not None

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
