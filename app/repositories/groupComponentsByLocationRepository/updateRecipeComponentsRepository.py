import gzip
import io

import xmltodict


class UpdateRecipeComponentsRepository:

    @staticmethod
    def update_board_components_in_selected_areas(xml_file: str, location_collection: list, suffix_for_update):

        with open(xml_file, 'rb') as file:
            data = xmltodict.parse(file)
            elements = data['Board']['Children']['a:Element']
            for element in elements:
                try:
                    if element['a:Name'][0] != 'T':
                        if isinstance(element['Bodies']['a:Body'], object):
                            x = float(element['RelativeLocation']['a:X'])
                            y = float(element['RelativeLocation']['a:Y'])
                            for location in location_collection:

                                if isinstance(x, float) and isinstance(y, float):
                                    if location.check_contains_component(x, y):

                                        component_in_location = str(element['a:Name'])
                                        print(component_in_location)
                                        element['a:TemplateName'] = element['a:TemplateName'] + suffix_for_update
                                        element['PackageName'] = element['PackageName'] + suffix_for_update
                                        element['PartNumber'] = element['PartNumber'] + suffix_for_update
                                        break

                except TypeError as e:
                    print(e)

        updated_xml = xmltodict.unparse(data, pretty=True)
        with open(xml_file, 'w') as file:
            file.write(updated_xml)

    @staticmethod
    def update_board_components_in_selected_areas_gzip_stream(gzip_stream, location_collection, suffix_for_update):

        with gzip.GzipFile(fileobj=gzip_stream, mode='rb') as gz:
            data = xmltodict.parse(gz)
        elements = data['Board']['Children']['a:Element']
        for element in elements:
            try:
                if element['a:Name'][0] != 'T':
                    if isinstance(element['Bodies']['a:Body'], object):
                        x = float(element['RelativeLocation']['a:X'])
                        y = float(element['RelativeLocation']['a:Y'])
                        for location in location_collection:

                            if isinstance(x, float) and isinstance(y, float):
                                if location.check_contains_component(x, y):
                                    element['a:TemplateName'] = element['a:TemplateName'] + suffix_for_update
                                    element['PackageName'] = element['PackageName'] + suffix_for_update
                                    element['PartNumber'] = element['PartNumber'] + suffix_for_update
                                    break

            except TypeError as e:
                print(e)

        updated_xml = xmltodict.unparse(data)
        updated_gzip_stream = io.BytesIO()
        with gzip.GzipFile(fileobj=updated_gzip_stream, mode='wb') as gz:
            gz.write(updated_xml.encode('utf-8'))
        updated_gzip_stream.seek(0)

        return updated_gzip_stream

    @staticmethod
    def prepare_locations_recipe_gzip_stream(gzip_stream):

        with gzip.GzipFile(fileobj=gzip_stream, mode='rb') as gz:
            data = xmltodict.parse(gz)
        data['Board']['Children']['a:Element'] = []
        updated_xml = xmltodict.unparse(data)
        updated_gzip_stream = io.BytesIO()
        with gzip.GzipFile(fileobj=updated_gzip_stream, mode='wb') as gz:
            gz.write(updated_xml.encode('utf-8'))
        updated_gzip_stream.seek(0)

        return updated_gzip_stream
