import pandas as pd
from numpy import ndarray


class MashFileRepository:

    def _get_mash_table(self, location: str) -> ndarray:

        return (pd.read_excel(location)).to_numpy()
