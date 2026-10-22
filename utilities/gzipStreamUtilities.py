import gzip
import io
import xmltodict


class GzipStreamUtilities:

    @staticmethod
    def parse_gzip_stream(gzip_path, mode='rb', parser=xmltodict):
        with open(gzip_path, 'rb') as f:
            gzip_stream = io.BytesIO(f.read())
            with gzip.GzipFile(fileobj=gzip_stream, mode=mode) as gz:
                data = xmltodict.parse(gz)

        return data

    @staticmethod
    def update_gzip_stream(data, gzip_path, mode='wb', parser=xmltodict):
        updated_xml = parser.unparse(data)
        updated_gzip_stream = io.BytesIO()
        with gzip.GzipFile(fileobj=updated_gzip_stream, mode=mode) as gz:
            gz.write(updated_xml.encode('utf-8'))
        updated_gzip_stream.seek(0)

        with open(gzip_path, 'wb') as f_updated:
            f_updated.write(updated_gzip_stream.read())
        return updated_gzip_stream
