class MashFileRepository:

    @staticmethod
    def get_mash_table(location: str):
        # Pandas is only needed while reading a workbook.
        # Mash rows only use the first 10 columns. Fall back when a sheet is narrower.
        import pandas as pd

        try:
            frame = pd.read_excel(location, usecols=range(10))
        except ValueError:
            frame = pd.read_excel(location)
        return frame.to_numpy()
