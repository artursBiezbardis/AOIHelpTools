import app.repositories.mashFileRepository.exportMashToExcelRepository as mashToExcel
import app.services.settingsService.settingsService as exportPath


class ExportToExcelService:
    path = exportPath.SettingsService().get_setting('-MASH_COMPARE_EXPORT_PATH-') + '\\mashCompareExport.xlsx'

    def create_excel(self, table_data: list, column_names: list):

        mashToExcel.ExportToExcelRepository().create_store_excel(self.path, table_data, column_names)
