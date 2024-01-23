import utilities.gzipStreamUtilities as streamGzip


class UpdateRecipeBoardComponentsFromMashRepository:

    @staticmethod
    def update_board_components(gzip_stream, update_dictionary):

        data = streamGzip.GzipStreamUtilities().parse_gzip_stream(gzip_stream)
        updated_data = UpdateRecipeBoardComponentsFromMashRepository.update_xml_data(data, update_dictionary)
        updated_gzip_stream = streamGzip.GzipStreamUtilities().update_gzip_stream(updated_data, gzip_stream)
        return updated_gzip_stream

    @staticmethod
    def update_xml_data(data, update_data):
        elements = data['Board']['Children']['a:Element']
        for element in elements:
            try:
                test = [element['a:Name']]
                if element['a:Name'] in update_data:
                    element['a:TemplateName'] = update_data[element['a:Name']]
                    element['PartNumber'] = update_data[element['a:Name']]
            except TypeError as e:
                print(e)
        return data
