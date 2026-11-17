import math

from openpyxl import Workbook
from openpyxl.styles import PatternFill


class ExportToExcelRepository:
    engine = 'openpyxl'

    def create_store_excel(self, path: str, data: list, columns_names, cells_with_differences=None):
        # Write with openpyxl and yellow-fill cells that differ between each compared pair.
        # cells_with_differences is ignored: the exported table itself is the source of truth.
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'mashCompare'

        for col_index, heading in enumerate(columns_names, start=1):
            sheet.cell(row=1, column=col_index, value=heading)

        for row_index, row in enumerate(data, start=2):
            for col_index, value in enumerate(row, start=1):
                sheet.cell(row=row_index, column=col_index, value=self._excel_value(value))

        self._paint_paired_row_differences(sheet, data)
        workbook.save(path)

    def _paint_paired_row_differences(self, sheet, data: list):
        row_index = 0
        while row_index + 1 < len(data):
            top = data[row_index]
            bottom = data[row_index + 1]
            if self._is_blank_row(top) or self._is_blank_row(bottom):
                row_index += 1
                continue

            excel_top = row_index + 2
            excel_bottom = excel_top + 1
            width = min(len(top), len(bottom), sheet.max_column)
            for col_index in range(width):
                # Mash filename always differs between the two files — never highlight it.
                if col_index == 0:
                    continue
                if self._values_equal(top[col_index], bottom[col_index]):
                    continue
                yellow = PatternFill(patternType='solid', fgColor='FFFF00')
                sheet.cell(row=excel_top, column=col_index + 1).fill = yellow
                sheet.cell(row=excel_bottom, column=col_index + 1).fill = PatternFill(
                    patternType='solid', fgColor='FFFF00'
                )
            row_index += 2

    @staticmethod
    def _is_blank_row(row) -> bool:
        if not row:
            return True
        first = row[0]
        return first is None or str(first).strip() == ''

    @staticmethod
    def _excel_value(value):
        if value is None:
            return None
        if isinstance(value, float) and math.isnan(value):
            return None
        text = str(value).strip()
        if text.lower() in ('nan', 'none'):
            return None
        return value

    @staticmethod
    def _values_equal(left, right) -> bool:
        def normalize(value):
            if value is None:
                return ''
            if isinstance(value, float) and math.isnan(value):
                return ''
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return float(value)
            text = str(value).strip()
            if text.lower() in ('', 'nan', 'none'):
                return ''
            try:
                return float(text.replace(',', '.'))
            except ValueError:
                return text.upper()

        return normalize(left) == normalize(right)
