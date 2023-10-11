import app.models.LocationsCollection as areaLocationCollection
import app.models.areaLocationModel as locationModel


class GroupComponentsByLocation:
    area_location_collection = areaLocationCollection.LocationsData([])

    def update_component_in_recipe(self):
        return

    def update_location_collection(self, location_data: locationModel.AreaLocation):
        self.area_location_collection.add_location_to_collection(location_data)

    def test(self):
        model1 = {
            'location_name': 'model1',
            'x': 100.1,
            'y': 100.00,
            'width': 300.1,
            'height': 300.01,
            'offset_x': 5,
            'offset_y': 6,
            'left_line_offset': 7,
            'right_line_offset': 8,
            'up_line_offset': 9,
            'down_line_offset': 10,
        }
        model2 = {
            'location_name': 'model2',
            'x': 100.2,
            'y': 100.02,
            'width': 300.2,
            'height': 300.02,
            'offset_x': 5.2,
            'offset_y': 6.6,
            'left_line_offset': 7.7,
            'right_line_offset': 8.9,
            'up_line_offset': 9.11,
            'down_line_offset': 10,
        }

        area1 = locationModel.AreaLocation(model1['location_name'], model1['x'], model1['y'], model1['width'],
                                           model1['height'],
                                           model1['offset_x'], model1['offset_y'], model1['left_line_offset'],
                                           model1['right_line_offset'],
                                           model1['up_line_offset'], model1['down_line_offset'])
        area2 = locationModel.AreaLocation(model1['location_name'], model1['x'], model1['y'], model1['width'],
                                           model1['height'],
                                           model1['offset_x'], model1['offset_y'], model1['left_line_offset'],
                                           model1['right_line_offset'],
                                           model1['up_line_offset'], model1['down_line_offset'])

        self.update_location_collection(area1)
        self.update_location_collection(area2)
        collection = self.area_location_collection
        test1 = '1234'
