import pandas as pd


class ExportToExcelRepository:
    engine = 'openpyxl'

    def create_store_excel(self, path: str, data: list, columns_names):
        data_frame = pd.DataFrame(data, columns=columns_names)

        # Save the DataFrame to an Excel file
        data_frame.to_excel(path, index=False, engine=self.engine)
