import app.models.recipeModels.xmlToDictBoardModel as boardModel


class XmlToDictComponentModel:

    def __init__(self,
                 board_model: boardModel.XmlToDictBoardModel,
                 new_component_data={},
                 component_data={}):
        self.new_component = new_component_data
        self.component = component_data if component_data else self.generate_component()
        
        self.get_component_name()
        self.get_part_name()
        self.generate_component()
        self.board = board_model

    def get_component(self):

        return self.component

    def get_component_name(self):

        return self.get_component()['a:Name']

    def get_part_name(self):

        return self.get_component()['a:TemplateName']

    def set_component_name(self, component_name):
        self.component['a:Name'] = component_name

    def set_part_name(self, part_name):
        self.component['PartNumber'] = part_name
        self.component['a:TemplateName'] = part_name
        self.component['Texts']['a:Text']['a:TemplateName'] = 'Part\\' + part_name + '\\Text_T1'



    def generate_component(self,
                         x_relative: float,
                         y_relative: float,
                         angle: int,
                         location_id: int,
                         location_link_id: int,
                         absolute_location=[]):

        component_name = self.get_component_name()
        part_name = self.get_part_name()
        board_nr = self.board.get_board_nr()
        board_location_x = self.board.get_board_position_x()
        board_location_y = self.board.get_board_position_y()
        board_angle = self.board.get_board_angle()
        absolute_x = float(absolute_location[0]) + board_location_x
        absolute_y = float(absolute_location[1]) + board_location_y
        absolute_angle = angle + board_angle if angle + board_angle < 360 else angle + board_angle - 360
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
                       'LogMessage': {
                           '@xmlns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.Framework.Common.Logging',
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