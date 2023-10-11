from dataclasses import dataclass
import app.models.areaLocationModel as areaLocation


@dataclass
class LocationsData:
    areaLocationCollection: list

    def add_location_to_collection(self, area_location: areaLocation.AreaLocation) -> None:
        self.areaLocationCollection.append(area_location)

    def get_location_collection(self):

        return self.areaLocationCollection
