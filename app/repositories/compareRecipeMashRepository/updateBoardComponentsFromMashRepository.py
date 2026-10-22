import copy

import utilities.gzipStreamUtilities as streamGzip
import app.models.areaLocationModel as fodLocationModel
import utilities.referenceComponentLocationUtilities as refComp


class UpdateRecipeBoardComponentsFromMashRepository:

    def update_board_components(self, gzip_stream, update_dictionary, mash_data, actions):
        data = {'data': streamGzip.GzipStreamUtilities().parse_gzip_stream(gzip_stream)}
        self._ensure_element_list(data)
        updated_data = self.update_existing_components(data, update_dictionary)
        donors = self._component_elements(updated_data)
        locator = refComp.ReferenceComponentLocationUtilities()
        transform = locator.find_board_transform(mash_data, updated_data)
        if actions.get('REMOVE_COMPONENTS'):
            updated_data = self.remove_components(updated_data, update_dictionary)
        if actions.get('REMOVE_FODS'):
            updated_data = self.remove_fods(updated_data)
        if actions.get('ADD_COMPONENTS'):
            updated_data = self.add_missing_components(
                updated_data, update_dictionary, mash_data, transform, donors, locator)
        updated_gzip_stream = streamGzip.GzipStreamUtilities().update_gzip_stream(updated_data['data'], gzip_stream)
        return updated_gzip_stream

    @staticmethod
    def update_existing_components(data, update_data):
        elements = data['data']['Board']['Children']['a:Element']
        for element in elements:
            try:
                if element['a:Name'] in update_data and update_data[element['a:Name']] != 'remove':
                    element['a:TemplateName'] = update_data[element['a:Name']]
                    element['PartNumber'] = update_data[element['a:Name']]
            except TypeError as e:
                print(e)
        return data

    @staticmethod
    def remove_components(data, update_data_for_remove):
        data['removed_components'] = {}
        elements = data['data']['Board']['Children']['a:Element']
        to_remove = []
        for index, element in enumerate(elements):
            try:
                if element['a:Name'] in update_data_for_remove and update_data_for_remove[element['a:Name']] == 'remove':
                    data['removed_components'][element['a:Name']] = element
                    to_remove.append(index)
            except TypeError as e:
                print(e)
        if isinstance(elements, list):
            for index in reversed(to_remove):
                del elements[index]
        return data

    @staticmethod
    def remove_fods(data):
        if 'removed_components' in data:
            elements = data['data']['Board']['Children']['a:Element']
            removed_points = None

            def removed_component_points():
                nonlocal removed_points
                if removed_points is None:
                    removed_points = []
                    for removed_component in data['removed_components'].values():
                        location = removed_component['RelativeLocation']
                        removed_points.append((float(location['a:X']), float(location['a:Y'])))
                return removed_points

            to_remove = []
            for index, element in enumerate(elements):
                try:
                    if 'FOD' in element['a:Name']:
                        fod_area_location = fodLocationModel.AreaLocation(
                                location_name=str(element['a:Name']),
                                x=float(element['RelativeLocation']['a:X']),
                                y=float(element['RelativeLocation']['a:Y']),
                                height=float(element['FODs']['a:FOD']['a:Shape']['Height']),
                                width=float(element['FODs']['a:FOD']['a:Shape']['Base']),
                                offset_x=float(0),
                                offset_y=float(0),
                                left_line_offset=float(0),
                                right_line_offset=float(0),
                                up_line_offset=float(0),
                                down_line_offset=float(0)
                        )
                        for point_x, point_y in removed_component_points():
                            if fod_area_location.check_contains_component(point_x, point_y):
                                to_remove.append(index)
                                break
                except TypeError as e:
                    print(e)
            if isinstance(elements, list):
                for index in reversed(to_remove):
                    del elements[index]

        return data

    def add_missing_components(self, data, update_dictionary, mash_data, transform, donors, locator=None):
        if locator is None:
            locator = refComp.ReferenceComponentLocationUtilities()

        elements = data['data']['Board']['Children']['a:Element']
        if not isinstance(elements, list):
            elements = locator.as_element_list(elements)
            data['data']['Board']['Children']['a:Element'] = elements

        existing_names = set()
        for element in elements:
            try:
                existing_names.add(str(element['a:Name']).strip())
            except (TypeError, KeyError):
                continue

        mash_components = mash_data.get('mash_data', {})
        candidates = []
        for name, part_name in update_dictionary.items():
            if part_name == 'remove' or name in existing_names or name not in mash_components:
                continue
            candidates.append((name, part_name))
        if not candidates:
            return data
        if not getattr(transform, 'found', False):
            print('Could not determine board position from mash and recipe coordinates; missing parts were not added to this board')
            return data

        for name, part_name in candidates:
            component = mash_components[name]
            donor = self._donor_for_part(donors, part_name)
            if donor is None:
                continue
            clone = copy.deepcopy(donor)
            try:
                recipe_x, recipe_y = locator.mash_to_recipe_position(
                    transform, float(component['x']), float(component['y']))
                clone['a:Name'] = name
                clone['a:TemplateName'] = part_name
                clone['PartNumber'] = part_name
                clone['RelativeLocation']['a:X'] = self._format_coord(recipe_x)
                clone['RelativeLocation']['a:Y'] = self._format_coord(recipe_y)
                if component.get('rotation') is not None:
                    clone['RelativeRotation'] = str(locator.mash_to_recipe_rotation(transform, component['rotation']))
            except (TypeError, KeyError, ValueError) as error:
                print(error)
                continue
            elements.append(clone)
            existing_names.add(name)
        return data

    @staticmethod
    def _ensure_element_list(data):
        children = data['data']['Board']['Children']
        elements = children.get('a:Element')
        if isinstance(elements, dict):
            children['a:Element'] = [elements]

    @classmethod
    def _component_elements(cls, data):
        elements = data['data']['Board']['Children']['a:Element']
        if isinstance(elements, dict):
            elements = [elements]
        elif not isinstance(elements, list):
            return []
        return [element for element in elements if cls._is_component_element(element)]

    @staticmethod
    def _is_component_element(element) -> bool:
        try:
            name = str(element['a:Name'])
            part = str(element.get('PartNumber', ''))
            location = element['RelativeLocation']
            float(location['a:X'])
            float(location['a:Y'])
        except (TypeError, KeyError, ValueError):
            return False
        if 'FOD' in name or 'Template_FOD' in part:
            return False
        return True

    @classmethod
    def _donor_for_part(cls, donors, part_name):
        part_key = str(part_name).strip().lower()
        exact = None
        partial = None
        fallback = None
        for element in donors:
            if not cls._is_component_element(element):
                continue
            donor_part = str(element.get('PartNumber', '')).strip().lower()
            if fallback is None:
                fallback = element
            if part_key and donor_part == part_key and exact is None:
                exact = element
            elif part_key and part_key in donor_part and partial is None:
                partial = element
        return exact or partial or fallback

    @staticmethod
    def _format_coord(value: float) -> str:
        text = f'{float(value):.4f}'.rstrip('0').rstrip('.')
        if text in ('', '-0'):
            return '0'
        return text
