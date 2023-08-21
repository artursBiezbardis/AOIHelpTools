import os


class Helpers:

    def get_filename_from_path(self,location):
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

    def add_to_env(self, key, value, env_file_path=".env"):
        """Add a key-value pair to a .env file."""
        with open(env_file_path, 'a') as file:
            file.write(f"\n{key}={value}")
