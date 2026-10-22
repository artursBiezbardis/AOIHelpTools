import utilities.gzipStreamUtilities as streamGzip
import app.models.areaLocationModel as fodLocationModel
import utilities.referenceComponentLocationUtilities as refComp


class UpdateRecipeBoardComponentsFromMashRepository:

    def update_board_components(self, gzip_stream, update_dictionary, mash_data, actions):
        data = {'data': streamGzip.GzipStreamUtilities().parse_gzip_stream(gzip_stream)}
        updated_data = self.update_existing_components(data, update_dictionary)
        angle = refComp.ReferenceComponentLocationUtilities().search_mash_angle_against_recipe(mash_data, data)
        if actions['REMOVE_COMPONENTS']:
            updated_data = self.remove_components(updated_data, update_dictionary)
        if actions['REMOVE_FODS']:
            updated_data = self.remove_fods(updated_data)
        updated_gzip_stream = streamGzip.GzipStreamUtilities().update_gzip_stream(updated_data['data'], gzip_stream)
        return updated_gzip_stream

    @staticmethod
    def update_existing_components(data, update_data):
        elements = data['data']['Board']['Children']['a:Element']
        for element in elements:
            try:
                if element['a:Name'] in update_data and update_data[element['a:Name']] != 'remove':
                    element['a:TemplateName'] = update_data[element['a:Name']]
                    element['PartNumber'] = update_data[element['a:Name']]
            except TypeError as e:
                print(e)
        return data

    @staticmethod
    def remove_components(data, update_data_for_remove):
        data['removed_components'] = {}
        elements = data['data']['Board']['Children']['a:Element']
        to_remove = []
        for index, element in enumerate(elements):
            try:
                if element['a:Name'] in update_data_for_remove and update_data_for_remove[element['a:Name']] == 'remove':
                    data['removed_components'][element['a:Name']] = element
                    to_remove.append(index)
            except TypeError as e:
                print(e)
        if isinstance(elements, list):
            for index in reversed(to_remove):
                del elements[index]
        return data

    @staticmethod
    def remove_fods(data):
        if 'removed_components' in data:
            elements = data['data']['Board']['Children']['a:Element']
            removed_points = None

            def removed_component_points():
                nonlocal removed_points
                if removed_points is None:
                    removed_points = []
                    for removed_component in data['removed_components'].values():
                        location = removed_component['RelativeLocation']
                        removed_points.append((float(location['a:X']), float(location['a:Y'])))
                return removed_points

            to_remove = []
            for index, element in enumerate(elements):
                try:
                    if 'FOD' in element['a:Name']:
                        fod_area_location = fodLocationModel.AreaLocation(
                                location_name=str(element['a:Name']),
                                x=float(element['RelativeLocation']['a:X']),
                                y=float(element['RelativeLocation']['a:Y']),
                                height=float(element['FODs']['a:FOD']['a:Shape']['Height']),
                                width=float(element['FODs']['a:FOD']['a:Shape']['Base']),
                                offset_x=float(0),
                                offset_y=float(0),
                                left_line_offset=float(0),
                                right_line_offset=float(0),
                                up_line_offset=float(0),
                                down_line_offset=float(0)
                        )
                        for point_x, point_y in removed_component_points():
                            if fod_area_location.check_contains_component(point_x, point_y):
                                to_remove.append(index)
                                break
                except TypeError as e:
                    print(e)
            if isinstance(elements, list):
                for index in reversed(to_remove):
                    del elements[index]

        return data
