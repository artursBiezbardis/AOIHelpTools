import gzip
import xmltodict


class GzipStreamUtilities:

    @staticmethod
    def parse_gzip_stream(gzip_path, mode='rb', parser=xmltodict):
        with gzip.open(gzip_path, mode) as gz:
            return parser.parse(gz)

    @staticmethod
    def update_gzip_stream(data, gzip_path, mode='wb', parser=xmltodict):
        updated_xml = parser.unparse(data)
        with gzip.open(gzip_path, mode) as gz:
            gz.write(updated_xml.encode('utf-8'))
