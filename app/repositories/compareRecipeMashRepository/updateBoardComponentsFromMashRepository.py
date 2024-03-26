import utilities.gzipStreamUtilities as streamGzip
import app.models.areaLocationModel as fodLocationModel
import utilities.referenceComponentLocationUtilities as refComp
import math
import utilities.fileAndFolderPathUtilities as pathUtils
import helpers.helpers as helper
import app.models.recipeModels.xmlToDictBoardModel as boardModel
import app.models.recipeModels.xmlToDictComponentModel as componentModel

class UpdateRecipeBoardComponentsFromMashRepository:

    def update_board_components(self, gzip_stream_path, update_dictionary, mash_data, actions, data_add_components):
        tmp_folder_path = pathUtils.FileAndFolderPathUtilities().get_folder_path_from_file_path(
            gzip_stream_path, 0)
        gzip_files = helper.Helpers().get_files_in_folder(tmp_folder_path)
        gzip_files.remove('Panel')
        first_board = '0.board'
        data = {'data': streamGzip.GzipStreamUtilities().parse_gzip_stream(gzip_stream_path)}
        updated_data = self.update_existing_components(data, update_dictionary)
        board_file = helper.Helpers().get_filename_from_path(gzip_stream_path)
        if actions['REMOVE_COMPONENTS']:
            updated_data = self.remove_components(updated_data['data'], update_dictionary)
        if actions['REMOVE_FODS']:
            updated_data = self.remove_fods(updated_data['data'])
        if actions['ADD_COMPONENTS']:
            if first_board == board_file:
                angle_and_relative_offset = refComp.ReferenceComponentLocationUtilities().validate_mash_angle_against_recipe(
                    mash_data, data)
                if not angle_and_relative_offset['valid']:
                    angle_and_relative_offset = refComp.ReferenceComponentLocationUtilities().validate_mash_angle_against_recipe(
                        mash_data, data, x_mirror=-1)
                if not angle_and_relative_offset['valid']:
                    angle_and_relative_offset = refComp.ReferenceComponentLocationUtilities().validate_mash_angle_against_recipe(
                        mash_data, data, y_mirror=-1)

                updated_data = self.get_reference_data(updated_data['data'], update_dictionary, angle_and_relative_offset, mash_data)
            else:
                updated_data['data_other_boards'] = data_add_components

            updated_data = self.add_components(updated_data)

        streamGzip.GzipStreamUtilities().update_gzip_stream(updated_data['data']['data'], gzip_stream_path)

        return updated_data['data_other_boards']

    @staticmethod
    def update_existing_components(data, update_data):
        elements = data['data']['Board']['Children']['a:Element']
        for element in elements:
            try:
                if element['a:Name'] in update_data and update_data[element['a:Name']]['action'] == 'update':
                    element['a:TemplateName'] = update_data[element['a:Name']]['part']
                    element['PartNumber'] = update_data[element['a:Name']]['part']
                    element['Texts']['a:Text']['a:TemplateName'] = 'Part\\' + element['PartNumber'] + '\\Text_T1'

            except TypeError as e:
                print(e)
        return {'data': data}

    @staticmethod
    def remove_components(data, update_data_for_remove):
        data['removed_components'] = {}
        elements = data['data']['Board']['Children']['a:Element']
        for element in elements.copy():
            try:
                if element['a:Name'] in update_data_for_remove and update_data_for_remove[element['a:Name']][
                    'action'] == 'remove':
                    data['removed_components'][element['a:Name']] = element
                    elements.remove(element)
            except TypeError as e:
                print(e)
        return {'data': data}

    @staticmethod
    def remove_fods(data):
        if 'removed_components' in data:
            elements = data['data']['Board']['Children']['a:Element']
            for element in elements.copy():
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
                        for key, removed_component in data['removed_components'].items():
                            if fod_area_location.check_contains_component(
                                    float(removed_component['RelativeLocation']['a:X']),
                                    float(removed_component['RelativeLocation']['a:Y'])):
                                if element in elements:
                                    elements.remove(element)
                except TypeError as e:
                    print(e)

        return {'data': data}

    def get_reference_data(self, data, update_data_to_add, coordinate_offsets, mash_data):
        action = 'add'
        board = boardModel.XmlToDictBoardModel(data['data'])
        elements = board.get_board_components()
        ids = self.get_part_ids(elements)
        location_id = int(ids[0]) + 2
        location_link_id = int(ids[1])
        parts_to_add = []
        data_other_boards = {}
        for part_to_add in update_data_to_add:
            if update_data_to_add[part_to_add]['action'] == action:
                if update_data_to_add[part_to_add]['part'] not in parts_to_add:
                    parts_to_add.append(update_data_to_add[part_to_add]['part'])

                coordinate_calculation = refComp.ReferenceComponentLocationUtilities().calculate_coordinates(
                    float(mash_data['mash_data'][part_to_add]['x']),
                    float(mash_data['mash_data'][part_to_add]['y']),
                    int(coordinate_offsets['result_angle']),
                    float(mash_data['mash_data'][part_to_add]['rotation']),
                    coordinate_offsets['x_mirror'],
                    coordinate_offsets['y_mirror']
                )

                component_name = part_to_add
                part_name = update_data_to_add[part_to_add]['part']
                x_relative = -(float(coordinate_calculation[0]) + float(coordinate_offsets['y_median']))*coordinate_offsets['x_mirror']
                y_relative = -(float(coordinate_calculation[1]) - float(coordinate_offsets['x_median']))*coordinate_offsets['y_mirror']
                part_angle_offset = int(mash_data['mash_data'][part_to_add]['rotation'])-coordinate_offsets['result_angle']+360
                part_angle = part_angle_offset if part_angle_offset < 360 else part_angle_offset-360

                try:

                    location_id = location_id + 1
                    location_link_id = location_link_id + 1
                    data_other_boards[component_name] = {'part_name': part_name,
                                                         'x_relative': x_relative,
                                                         'y_relative': y_relative,
                                                         'angle': part_angle,
                                                         'location_id': location_id,
                                                         'location_link_id': location_link_id,
                                                         'x_mirror': coordinate_offsets['x_mirror'],
                                                         'y_mirror': coordinate_offsets['y_mirror'],

                                                         }
                    location_id = location_id + 1

                except TypeError as e:
                    print(e)

        return {'data': data, 'parts_to_add': parts_to_add, 'data_other_boards': data_other_boards}

    @staticmethod
    def get_part_ids(elements):
        last_element = list(elements)[-1]
        id = last_element['a:ID']
        location_link_id = last_element['a:LocationLinkID']
        return [int(id), int(location_link_id)]

    def add_components(self, updated_data):
        tmp_component_suffix = 'prep_'

        new_data = updated_data
        board = boardModel.XmlToDictBoardModel(updated_data['data']['data'])
        elements = board.get_board_components()
        board_nr = board.get_board_nr()
        board_angle = board.get_board_angle()
        board_position = [board.get_board_position_x(), board.get_board_position_y(), board_angle]
        board_height = board.get_board_height()
        board_width = board.get_board_width()
        for component_name, new_comp_data in updated_data['data_other_boards'].items():
            component_name = tmp_component_suffix + component_name

            x_relative = new_comp_data['x_relative'] if new_comp_data['x_mirror'] == 1 else self.calculate_relative_mirror(new_comp_data['x_relative'], board_width)

            y_relative = new_comp_data['y_relative'] if new_comp_data['y_mirror'] == 1 else self.calculate_relative_mirror(new_comp_data['y_relative'], board_height)

            absolute_location = refComp.ReferenceComponentLocationUtilities().calculate_coordinates(
                x_relative,
                y_relative,
                board_angle,
                0)

            new_element = self.generate_element(board_nr,
                                                board_position,
                                                component_name,
                                                new_comp_data['part_name'],
                                                x_relative,
                                                y_relative,
                                                int(new_comp_data['angle']),
                                                new_comp_data['location_id'],
                                                new_comp_data['location_link_id'],
                                                absolute_location)
            elements.append(new_element)

        board.set_board_components(elements)
        new_data['data']['data'] = board.data

        return new_data



    @staticmethod
    def calculate_relative_mirror(relative_axe_value, board_axe_length):

        return board_axe_length - relative_axe_value

    @staticmethod
    def calculate_absolut_location(relative_x, relative_y, board_angle_degrees, x_mirror, y_mirror):
        angle_rad = math.radians(board_angle_degrees)
        absolute_x = x_mirror * (relative_x * math.cos(angle_rad) - relative_y * math.sin(angle_rad))
        absolute_y = y_mirror * (relative_x * math.sin(angle_rad) + relative_y * math.cos(angle_rad))

        return [absolute_x, absolute_y]

    @staticmethod
    def calculate_reference_board_rotate_by_center(board_angle, board_height, board_width, board_position):
        calculated_position = board_position
        if board_angle == 180:
            calculated_position = [board_position[0]-board_width, board_position[1]-board_height]
        elif board_angle == 90:
            calculated_position = [board_position[0]-board_height, board_position[1]]
        elif board_angle == 270:
            calculated_position = [board_position[0], board_position[1]-board_width]
        return calculated_position

    @staticmethod
    def generate_element(board_nr, board_location, component_name, part_name, x_relative: float, y_relative: float,
                         angle: int,
                         location_id: int, location_link_id: int, absolute_location=[]):
        absolute_x = float(absolute_location[0]) + float(board_location[0])
        absolute_y = float(absolute_location[1]) + float(board_location[1])

        absolute_angle = angle+board_location[2] if angle+board_location[2] < 360 else angle+board_location[2]-360

        package_name = 'generic_template'
        element = {'@i:type': 'Component', 'LogMessage': {
            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
            '#text': 'Panel.' + board_nr + '.' + component_name}, 'LogRecipeDataName': {
            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
            '#text': board_nr + '.' + component_name}, 'LogTemplateName': {
            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                   'a:ID': location_id,
                   'a:LocationLinkID': location_link_id, 'a:Name': component_name, 'a:Position': {
                'LogMessage': {'@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                               '#text': 'Panel.' + board_nr + '.' + component_name + '.Position'},
                'LogRecipeDataName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                    '#text': board_nr + '.' + component_name}, 'LogTemplateName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                'a:X': absolute_x,
                'a:Y': absolute_y},
                'a:RotationZ': absolute_angle,
                   'a:Task': {
                'LogMessage': {'@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                               '#text': 'Panel.' + board_nr + '.' + component_name + '.Task'}, 'LogRecipeDataName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                    '#text': board_nr + '.' + component_name}, 'LogTemplateName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                'a:Inspect': 'true', 'a:InspectMode': 'FavorSpeed', 'a:Name': None}, 'a:TemplateName': part_name,
                   'Barcodes': None, 'Bodies': {'a:Body': {
                'LogMessage': {'@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                               '#text': 'Panel.' + board_nr + '.' + component_name + '.Body'}, 'LogRecipeDataName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                    '#text': board_nr + '.' + component_name}, 'LogTemplateName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                'a:ID': (int(location_id) + 1), 'a:LocationLinkID': '0', 'a:Name': 'Body',
                'a:Position': {'LogMessage': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                    '#text': 'Panel.' + board_nr + '.' + component_name + '.Body.Position'}, 'LogRecipeDataName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                    '#text': board_nr + '.' + component_name}, 'LogTemplateName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'a:X': float(x_relative),
                    'a:Y': float(y_relative)},
                'a:RotationZ': absolute_angle,
                'a:Task': {'LogMessage': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                    '#text': 'Panel.' + board_nr + '.' + component_name + '.Body.Task'}, 'LogRecipeDataName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                    '#text': board_nr + '.' + component_name}, 'LogTemplateName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'a:Inspect': 'true', 'a:InspectMode': 'FavorSpeed', 'a:Name': None},
                'a:TemplateName': 'Pkg\\' + package_name + '\\Body_T1', 'a:IncludedInCurrentVariant': 'true',
                'a:InspectionArea': {'LogMessage': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'LogRecipeDataName': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'LogTemplateName': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'a:Shape': {'@i:type': 'Rectangle', 'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                                'LogRecipeDataName': {
                                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                                'LogTemplateName': {
                                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                                'Base': '4.6087303279937331', 'Height': '4.1373829080852857'}},
                'a:Shape': {'@i:type': 'Rectangle', 'LogMessage': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                            'LogRecipeDataName': {
                                '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                            'LogTemplateName': {
                                '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                            'Base': '3.0724868853291554', 'Height': '2.7582552720568572'}, 'a:Tolerance': {
                    'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'LogRecipeDataName': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'LogTemplateName': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'a:Area': {'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogRecipeDataName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogTemplateName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'}},
                    'a:Bridging': {'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogRecipeDataName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogTemplateName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'}},
                    'a:Height': {'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogRecipeDataName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogTemplateName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'}},
                    'a:Lighting': {'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogRecipeDataName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogTemplateName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'a:IllumType': '-1', 'a:LightToDark': 'false'}, 'a:Offset': {'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogRecipeDataName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogTemplateName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'}},
                    'a:Volume': {'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogRecipeDataName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogTemplateName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'}}}}},
                   'CaptureInCenter': 'false', 'ComponentReferenceAreas': None,
                   'CustomerizeHeightImageOptions': 'false', 'FODs': None, 'Fiducials': None, 'Gaps': None,
                   'GroupIndex': '0', 'HeightImageOptions': {'@i:nil': 'true'}, 'IncludedInCurrentVariant': 'false',
                   'Leads': None, 'PackageName': package_name, 'PackageTypeName': None, 'Pads': None,
                   'PartNumber': part_name, 'Polarities': None, 'ReferenceAreas': None, 'RelativeLocation': {
                'LogMessage': {'@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                               '#text': 'Panel.' + board_nr + '.' + component_name + '.RelativeLocation'},
                'LogRecipeDataName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
                    '#text': board_nr + '.' + component_name}, 'LogTemplateName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                'a:X': x_relative, 'a:Y': y_relative}, 'RelativeRotation': angle,
                   'SaveImageAfterInspection': 'false', 'SideViewImageOptions': {'@i:nil': 'true'},
                   'SideViewImagePerspectiveCorrection': 'false', 'SolderPastes': None, 'Texts': None, 'Tolerance': {
                'LogMessage': {'@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                'LogRecipeDataName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                'LogTemplateName': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                'a:ComplianceTolerance': {'LogMessage': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'LogRecipeDataName': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'LogTemplateName': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'a:Area': {'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogRecipeDataName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogTemplateName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'}},
                    'a:Height': {'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogRecipeDataName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogTemplateName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'}},
                    'a:Volume': {'LogMessage': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogRecipeDataName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                        'LogTemplateName': {
                            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'}}},
                'a:PadRollupTally': {'LogMessage': {
                    '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'LogRecipeDataName': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                    'LogTemplateName': {
                        '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'}}},
                   'UseAsStitchFeature': 'false', 'WireGroups': None}
        return element

    @staticmethod
    def xml_template_panel_parts(part_name):
        element = {'b:Key': part_name, 'b:Value': {'@xmlns:c': 'http://www.cyberoptics.com'
                                                               '/templatepropertydecorator', 'LogMessage': {
            '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                                                   'LogRecipeDataName': {'@xmlns':
                                                                             'http://schemas.datacontract.org'
                                                                             '/2004/07/CO.Phoenix.Framework.Common.Logging'},
                                                   'LogTemplateName': {
                                                       '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                                                   'c:TemplateLocation': 'Shared', 'c:_lastCommitRecords': None}}

        return element

    @staticmethod
    def xml_template_panel_package():
        element = {'b:Key': 'generic_template',
                   'b:Value': {'@xmlns:c': 'http://www.cyberoptics.com/templatepropertydecorator', 'LogMessage': {
                       '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                               'LogRecipeDataName': {
                                   '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                               'LogTemplateName': {
                                   '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging'},
                               'c:TemplateLocation': 'Shared', 'c:_lastCommitRecords': None}}

        return element
