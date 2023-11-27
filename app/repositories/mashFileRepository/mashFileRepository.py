import pandas as pd
from numpy import ndarray


class MashFileRepository:

    @staticmethod
    def get_mash_table(location: str) -> ndarray:

        return (pd.read_excel(location)).to_numpy()
