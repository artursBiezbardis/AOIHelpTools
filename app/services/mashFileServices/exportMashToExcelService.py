import os

import app.repositories.mashFileRepository.exportMashToExcelRepository as mashToExcel
import app.services.settingsService.settingsService as exportPath


class ExportToExcelService:
    def __init__(self):
        export_folder = exportPath.SettingsService().get_setting('-MASH_COMPARE_EXPORT_PATH-')
        self.path = os.path.join(export_folder, 'mashCompareExport.xlsx')

    def create_excel(self, table_data: list, column_names: list, cells_with_differences=None):
        mashToExcel.ExportToExcelRepository().create_store_excel(
            self.path,
            table_data,
            column_names,
            cells_with_differences,
        )
