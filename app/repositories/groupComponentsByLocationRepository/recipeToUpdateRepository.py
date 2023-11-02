import xmltodict
from collections.abc import Sequence, Mapping

class RecipeToUpdateRepository:

    def update_board_components_in_selected_areas(self, xml_file: str, location_collection: list, suffix_for_update):

        with open(xml_file, 'rb') as file:
            data = xmltodict.parse(file)
            elements = data['Board']['Children']['a:Element']
            count = 1
            for element in elements:
                try:
                    if element['a:Name'][0] != 'T':
                        component_in_location = False
                        if isinstance(element['Bodies']['a:Body'], object):
                            x = float(element['Bodies']['a:Body']['a:Position']['a:X'])
                            y = float(element['Bodies']['a:Body']['a:Position']['a:Y'])
                            for location in location_collection:

                                if isinstance(x, float) and isinstance(y, float):
                                    if location.check_contains_component(x, y):

                                        component_in_location = str(element['a:Name'])
                                        print(component_in_location)
                                        element['a:TemplateName'] = element['a:TemplateName'] + suffix_for_update
                                        element['PackageName'] = element['PackageName'] + suffix_for_update
                                        element['PartNumber'] = element['PartNumber'] + suffix_for_update

                                        count+=1
                                        break

                except TypeError as e:
                    print(e)

        updated_xml = xmltodict.unparse(data, pretty=True)
        with open(xml_file, 'w') as file:
            file.write(updated_xml)
