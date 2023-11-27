import xmltodict
import gzip
import io


class UpdateRecipesRepository:

    def stream_gzip_for_update(self, part_name, package_name, recipe_path):
        with open(recipe_path + '/tmp/Panel', 'rb') as f:
            gzip_stream = io.BytesIO(f.read())

        updated_gzip_stream = self.update_panel_gzip_stream(gzip_stream, part_name, package_name)

        with open(recipe_path + '/tmp/Panel', 'wb') as f_updated:
            f_updated.write(updated_gzip_stream.read())

    @staticmethod
    def update_panel_gzip_stream(gzip_stream, part_name, package_name):

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

        updated_xml = xmltodict.unparse(data)
        updated_gzip_stream = io.BytesIO()
        with gzip.GzipFile(fileobj=updated_gzip_stream, mode='wb') as gz:
            gz.write(updated_xml.encode('utf-8'))
        updated_gzip_stream.seek(0)

        return updated_gzip_stream
