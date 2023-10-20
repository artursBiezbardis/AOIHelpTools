from lxml import etree
import xmltodict


class RecipeToUpdateRepository:

    def get_area_location_data(self, xml_file: str,):
        tree = etree.parse(xml_file)
        root = tree.getroot()
        # Define the namespace
        ns = {'ns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.CyberDataModel.RecipeData'}

        # Find all elements with the namespace
        elements = root.xpath('//Element')

        for element in elements:
            ns = {'ns': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.CyberDataModel.RecipeData'}
            print(ns)
            name = element.find('.//Name').text
            relative_position_x = float(element.find('.//X').text)
            relative_position_y = float(element.find('.//Y').text)
            ns = {'a': 'http://schemas.datacontract.org/2004/07/CO.Phoenix.CyberDataModel.RecipeData'}
            print(ns)
            shape_base = root.find('.//Body/Shape/*[1]')

            shape_height = element.find('.//Height').text

            print(f"Name: {name}")
            print(f"Relative Position: ({relative_position_x}, {relative_position_y})")
            print(f"Shape Base: {shape_base}")
            print(f"Shape Height: {shape_height}\n")




