import xmltodict
import gzip
import io


class UpdateRecipesRepository:

    def update_panel_gzip_stream(self, gzip_stream, part_name, package_name, selection):
        # Decompress the gzip stream
        with gzip.GzipFile(fileobj=gzip_stream, mode='rb') as gz:
            data = xmltodict.parse(gz)

        for element in data['Panel']['PartLibrary']['a:RootTemplates']['a:_templatePropertyDecorators']['b:KeyValueOfstringTemplatePropertyDecoratorDVHnpzMe']:
            try:
                if element['b:Key'] == part_name:
                    element['b:Value']['c:TemplateLocation'] = 'Shared'
            except TypeError as e:
                print(e)

        for element in data['Panel']['PackageLibrary']['a:RootTemplates']['a:_templatePropertyDecorators']['b:KeyValueOfstringTemplatePropertyDecoratorDVHnpzMe']:
            try:
                if element['b:Key'] == package_name:
                    element['b:Value']['c:TemplateLocation'] = 'Shared'
            except TypeError as e:
                print(e)
        # Instead of writing to a file, you unparse the XML and return the updated XML as a string
        updated_xml = xmltodict.unparse(data)

        # Create a new gzip stream for the updated XML
        updated_gzip_stream = io.BytesIO()
        with gzip.GzipFile(fileobj=updated_gzip_stream, mode='wb') as gz:
            gz.write(updated_xml.encode('utf-8'))  # Write the updated XML string as bytes

        # Return the updated gzip stream
        updated_gzip_stream.seek(0)
        return updated_gzip_stream