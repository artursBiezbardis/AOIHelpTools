import zipfile
import shutil


class CompressExtractZipUtilities:

    @staticmethod
    def extract_zip(path_to_recipe, extract_path):
        with zipfile.ZipFile(path_to_recipe, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    @staticmethod
    def compress_zip(path, file_name):
        file_path = path + '\\' + file_name
        shutil.make_archive(file_path.replace('.recipe', ''), 'zip', path)

    @staticmethod
    def compress_zip_files(resulting_file_path: str, list_of_file_names: list, file_folder_path: str):
        with zipfile.ZipFile(resulting_file_path, 'w') as zipf:
            for gzip_file in list_of_file_names:
                zipf.write(file_folder_path + '/' + gzip_file, gzip_file)

