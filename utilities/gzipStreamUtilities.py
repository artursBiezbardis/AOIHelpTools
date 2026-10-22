import gzip
import io
import xmltodict


class GzipStreamUtilities:

    @staticmethod
    def parse_gzip_stream(gzip_path, mode='rb', parser=xmltodict):
        with gzip.open(gzip_path, mode) as gz:
            return parser.parse(gz)

    @staticmethod
    def update_gzip_stream(data, gzip_path, mode='wb', parser=xmltodict):
        updated_xml = parser.unparse(data).encode('utf-8')
        updated_gzip_stream = io.BytesIO()
        with gzip.GzipFile(fileobj=updated_gzip_stream, mode=mode) as gz:
            gz.write(updated_xml)
        compressed = updated_gzip_stream.getvalue()
        with open(gzip_path, 'wb') as f_updated:
            f_updated.write(compressed)
        return updated_gzip_stream
