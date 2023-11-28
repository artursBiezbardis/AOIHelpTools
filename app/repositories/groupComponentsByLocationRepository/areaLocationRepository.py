import xmltodict
import app.models.LocationsCollection as areaLocationCollection
import app.models.areaLocationModel as locationModel


class AreaLocationRepository:

    area_location_collection = areaLocationCollection.LocationsData([])

    def get_area_location_data(self, xml_file: str, view_input) -> areaLocationCollection.LocationsData:

        with open(xml_file, 'rb') as file:
            data = xmltodict.parse(file)
            elements = data['Board']['Children']['a:Element']
            if isinstance(elements, list):
                for element in elements:
                    self.area_location_collection.add_location_to_collection(
                        locationModel.AreaLocation(
                            location_name=str(element['a:Name']),
                            x=float(element['RelativeLocation']['a:X']),
                            y=float(element['RelativeLocation']['a:Y']),
                            height=float(element['Bodies']['a:Body']['a:Shape']['Height']),
                            width=float(element['Bodies']['a:Body']['a:Shape']['Base']),
                            offset_x=float(view_input['-X_OFFSET-']),
                            offset_y=float(view_input['-Y_OFFSET-']),
                            left_line_offset=float(view_input['-LEFT_OFFSET-']),
                            right_line_offset=float(view_input['-RIGHT_OFFSET-']),
                            up_line_offset=float(view_input['-UP_OFFSET-']),
                            down_line_offset=float(view_input['-DOWN_OFFSET-'])
                        ))

            elif isinstance(elements, dict):
                self.area_location_collection.add_location_to_collection(
                    locationModel.AreaLocation(
                        location_name=str(elements['a:Name']),
                        x=float(elements['RelativeLocation']['a:X']),
                        y=float(elements['RelativeLocation']['a:Y']),
                        height=float(elements['Bodies']['a:Body']['a:Shape']['Height']),
                        width=float(elements['Bodies']['a:Body']['a:Shape']['Base']),
                        offset_x=float(view_input['-X_OFFSET-']),
                        offset_y=float(view_input['-Y_OFFSET-']),
                        left_line_offset=float(view_input['-LEFT_OFFSET-']),
                        right_line_offset=float(view_input['-RIGHT_OFFSET-']),
                        up_line_offset=float(view_input['-UP_OFFSET-']),
                        down_line_offset=float(view_input['-DOWN_OFFSET-'])
                    ))

            return self.area_location_collection
