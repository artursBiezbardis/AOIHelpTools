import app.repositories.mashFileRepository.mashFileRepository as mashFileRepo


class MashFileService:

    def __init__(self, mashFileRepo: mashFileRepo.MashFileRepository):
        self.mashFileRepo = mashFileRepo

    def extract_mash_data(self, location) -> array:


        return self.mashFileRepo._get_mash_table(location)
