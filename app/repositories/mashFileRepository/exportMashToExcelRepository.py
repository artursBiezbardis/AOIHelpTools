import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill


class ExportToExcelRepository:
    engine = 'openpyxl'
    # Mash filename is inserted at column 0 after diffs are located, so shift by one.
    # Excel is 1-based and row 1 is the header written by pandas.
    _MASH_COLUMN_OFFSET = 1
    _HEADER_ROW_OFFSET = 1
    _yellow = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

    def create_store_excel(self, path: str, data: list, columns_names, cells_with_differences=None):
        data_frame = pd.DataFrame(data, columns=columns_names)
        data_frame.to_excel(path, index=False, engine=self.engine)
        if cells_with_differences:
            self._paint_difference_cells(path, cells_with_differences)

    def _paint_difference_cells(self, path: str, cells_with_differences: list):
        workbook = load_workbook(path)
        sheet = workbook.active
        max_row = sheet.max_row
        max_col = sheet.max_column

        for entry in cells_with_differences:
            if not entry:
                continue
            excel_row = entry[0] + self._HEADER_ROW_OFFSET
            if excel_row < 2 or excel_row > max_row:
                continue
            for column_index in entry[1:]:
                excel_col = column_index + self._MASH_COLUMN_OFFSET + 1
                if 1 <= excel_col <= max_col:
                    sheet.cell(row=excel_row, column=excel_col).fill = self._yellow

        workbook.save(path)
