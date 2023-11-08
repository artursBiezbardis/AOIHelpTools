import zipfile
import shutil
import gzip


class CompressAndExtractRecipesHelper:

    @staticmethod
    def extract_gzip(path, file_name, out_put_path=''):
        file_path = path + file_name
        with gzip.open(file_path, 'rb') as gz_file:
            file_content = gz_file.read()
        with open(path + out_put_path, 'wb') as out_put_file:
            out_put_file.write(file_content)

    @staticmethod
    def compress_gzip(path, file_name, out_put_path=''):
        file_path = path + file_name
        with open(file_path, 'rb') as gz_file:
            file_content = gz_file.read()
        with gzip.open(out_put_path, 'wb') as out_put_file:
            out_put_file.write(file_content)


    @staticmethod
    def extract_zip(path, file_name):
        file_path = path + '\\' + file_name
        extract_path = path + '\\tmp'
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    @staticmethod
    def compress_zip(path, file_name):
        file_path = path + '\\' + file_name
        shutil.make_archive(file_path.replace('.recipe', ''), 'zip', path)

