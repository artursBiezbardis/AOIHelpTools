import os
import shutil
from datetime import datetime


class BackUpUtilities:

    @staticmethod
    def create_backup_for_file(backup_dir, file_path, backup_name=''):
        time_now = datetime.now()
        dir_path = os.path.dirname(file_path)
        directory_list = os.listdir(dir_path)
        backup_dir_name = os.path.basename(backup_dir)
        if backup_dir_name not in directory_list:
            os.mkdir(backup_dir)
        backup_path = f'{backup_dir}/'+backup_name + time_now.strftime('%d-%m-%Y-%H_%M_%S.recipe')
        shutil.move(file_path, backup_path)
