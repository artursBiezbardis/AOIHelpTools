import app.repositories.mashFileRepository.exportMashToExcelRepository as mashToExcel


class ExportToExcelService:
    path = ''

    def create_excel(self, table_data: list, column_names :list):

        path = self.format_mash_path()
        mashToExcel.ExportToExcelRepository().create_store_excel(path, table_data, column_names)

    def format_mash_path(self):
        return 'C:\\Users\\arturs.biezbardis\\Desktop\\test.xlsx'