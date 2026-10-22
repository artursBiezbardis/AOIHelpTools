import xmltodict
import app.models.LocationsCollection as areaLocationCollection
import app.models.areaLocationModel as locationModel


class AreaLocationRepository:

    area_location_collection = areaLocationCollection.LocationsData([])

    def get_area_location_data(self, xml_file: str, view_input) -> areaLocationCollection.LocationsData:
        offset_x = float(view_input['-X_OFFSET-'])
        offset_y = float(view_input['-Y_OFFSET-'])
        left_line_offset = float(view_input['-LEFT_OFFSET-'])
        right_line_offset = float(view_input['-RIGHT_OFFSET-'])
        up_line_offset = float(view_input['-UP_OFFSET-'])
        down_line_offset = float(view_input['-DOWN_OFFSET-'])

        def add_element(element):
            self.area_location_collection.add_location_to_collection(
                locationModel.AreaLocation(
                    location_name=str(element['a:Name']),
                    x=float(element['RelativeLocation']['a:X']),
                    y=float(element['RelativeLocation']['a:Y']),
                    height=float(element['Bodies']['a:Body']['a:Shape']['Height']),
                    width=float(element['Bodies']['a:Body']['a:Shape']['Base']),
                    offset_x=offset_x,
                    offset_y=offset_y,
                    left_line_offset=left_line_offset,
                    right_line_offset=right_line_offset,
                    up_line_offset=up_line_offset,
                    down_line_offset=down_line_offset,
                )
            )

        with open(xml_file, 'rb') as file:
            data = xmltodict.parse(file)
            elements = data['Board']['Children']['a:Element']
            if isinstance(elements, dict):
                add_element(elements)
            elif isinstance(elements, list):
                for element in elements:
                    add_element(element)

            return self.area_location_collection
