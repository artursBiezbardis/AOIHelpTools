from collections import Counter
import math
import app.models.recipeModels.xmlToDictBoardModel as boardModel


class ReferenceComponentLocationUtilities:
    ALLOWANCE_OFFSET_X = 0.4
    ALLOWANCE_OFFSET_Y = 0.4
    COLLECT_DIFF_LIMIT = 100
    MASH_BOARD_ANGLES_SEARCH_LIST = [0, 90, 180, 270]
    RESULTS_CONFIDENCE_THRESHOLD = 0.9

    def search_mash_angle_against_recipe(self, mash_data, board_data):

        angle_and_relative_offset = self.validate_mash_angle_against_recipe(
            mash_data, board_data)
        if not angle_and_relative_offset['valid']:
            angle_and_relative_offset = self.validate_mash_angle_against_recipe(
                mash_data, board_data, x_mirror=-1)
        if not angle_and_relative_offset['valid']:
            angle_and_relative_offset = self.validate_mash_angle_against_recipe(
                mash_data, board_data, y_mirror=-1)

        return angle_and_relative_offset

    def calculate_reference_board_coordinates(self, board_data, update_data_to_add, coordinate_offsets, mash_data):
        action = 'add'
        board = boardModel.XmlToDictBoardModel(board_data['data'])
        elements = board.get_board_components()
        ids = self.get_part_ids(elements)
        location_id = int(ids[0]) + 2
        location_link_id = int(ids[1])
        parts_to_add = []
        data_other_boards = {}
        for part_to_add in update_data_to_add:
            if update_data_to_add[part_to_add]['action'] == action:
                if update_data_to_add[part_to_add]['part'] not in parts_to_add:
                    parts_to_add.append(update_data_to_add[part_to_add]['part'])
                #     create mash part model
                coordinate_calculation = self.calculate_coordinates(
                    float(mash_data['mash_data'][part_to_add]['x']),
                    float(mash_data['mash_data'][part_to_add]['y']),
                    int(coordinate_offsets['result_angle']),
                    float(mash_data['mash_data'][part_to_add]['rotation']),
                    coordinate_offsets['x_mirror'],
                    coordinate_offsets['y_mirror']
                )

                component_name = part_to_add
                part_name = update_data_to_add[part_to_add]['part']
                x_relative = -(float(coordinate_calculation[0]) + float(coordinate_offsets['y_median'])) * \
                             coordinate_offsets['x_mirror']
                y_relative = -(float(coordinate_calculation[1]) - float(coordinate_offsets['x_median'])) * \
                             coordinate_offsets['y_mirror']
                part_angle_offset = int(mash_data['mash_data'][part_to_add]['rotation']) - coordinate_offsets[
                    'result_angle'] + 360
                part_angle = part_angle_offset if part_angle_offset < 360 else part_angle_offset - 360

                try:

                    location_id = location_id + 1
                    location_link_id = location_link_id + 1
                    data_other_boards[component_name] = {'part_name': part_name,
                                                         'x_relative': x_relative,
                                                         'y_relative': y_relative,
                                                         'angle': part_angle,
                                                         'location_id': location_id,
                                                         'location_link_id': location_link_id,
                                                         'x_mirror': coordinate_offsets['x_mirror'],
                                                         'y_mirror': coordinate_offsets['y_mirror'],

                                                         }
                    location_id = location_id + 1

                except TypeError as e:
                    print(e)

        return {'data': board_data, 'parts_to_add': parts_to_add, 'data_other_boards': data_other_boards}

    @staticmethod
    def get_part_ids(elements):
        last_element = list(elements)[-1]
        id = last_element['a:ID']
        location_link_id = last_element['a:LocationLinkID']
        return [int(id), int(location_link_id)]

    def calculate_statistical_component_angle_diff(self, mash_data: dict, recipe_data: dict):
        count = 0
        angle_differences = []
        for key, component in mash_data.items():
            if key in recipe_data:
                angle_difference: float = component['angle'] - recipe_data[key]['angle']
                angle_differences.append(angle_difference)
                if count >= self.COLLECT_DIFF_LIMIT:
                    break
                count += 1

        result = Counter(angle_differences)
        highest_count_diff_angle = max(result, key=result.get)

        return highest_count_diff_angle

    def validate_mash_angle_against_recipe(self, mash_data: dict, recipe_data: dict, x_mirror=1, y_mirror=1) -> dict:
        result_angle = 360
        mash_data = self.mash_payload_from_model(mash_data)
        recipe_elements = self.recipe_elements(recipe_data)

        for angle in self.MASH_BOARD_ANGLES_SEARCH_LIST:
            reference_mash_data = {}
            angle_radians = math.radians(angle)
            count = 1
            results_x = []
            results_y = []
            for data in recipe_elements:
                if isinstance(data, str) or data['a:Name'] not in mash_data['mash_data']:
                    continue
                x_reducer = x_mirror * float(data['RelativeLocation']['a:X']) * math.cos(angle_radians) - y_mirror * float(data['RelativeLocation']['a:Y']) * math.sin(angle_radians)
                y_reducer = x_mirror * float(data['RelativeLocation']['a:X']) * math.sin(angle_radians) + y_mirror * float(data['RelativeLocation']['a:Y']) * math.cos(angle_radians)
                reference_mash_data[data['a:Name']] = mash_data['mash_data'][data['a:Name']]

                result_x = float(mash_data['mash_data'][data['a:Name']]['x']) - x_reducer
                result_y = float(mash_data['mash_data'][data['a:Name']]['y']) - y_reducer
                results_x.append(result_x)
                results_y.append(result_y)
                if count >= self.COLLECT_DIFF_LIMIT:
                    break
                count += 1

            if not results_x or not results_y:
                continue
            x_median = (sorted(results_x))[(len(results_x)) // 2]
            y_median = (sorted(results_y))[(len(results_y)) // 2]
            validate_x = self.check_if_list_values_in_range(results_x, x_median, self.ALLOWANCE_OFFSET_X, self.RESULTS_CONFIDENCE_THRESHOLD)
            validate_y = self.check_if_list_values_in_range(results_y, y_median, self.ALLOWANCE_OFFSET_Y, self.RESULTS_CONFIDENCE_THRESHOLD)
            if validate_y and validate_x:
                result_angle = angle

                return {'result_angle': result_angle, 'x_median': x_median, 'y_median': y_median, 'x_mirror': x_mirror, 'y_mirror': y_mirror, 'valid': True, }

        return {'result_angle': result_angle, 'x_median': 0.0, 'y_median': 0.0, 'x_mirror': x_mirror, 'y_mirror': y_mirror, 'valid': False}

    @staticmethod
    def mash_payload_from_model(mash_data):
        if hasattr(mash_data, 'update_mash_model_from_component_dict'):
            rows = mash_data.update_mash_model_from_component_dict()
            coordinates = {}
            for name, row in rows.items():
                if isinstance(row, str):
                    continue
                if isinstance(row, dict) and 'x' in row:
                    coordinates[name] = row
                elif isinstance(row, (list, tuple)) and len(row) > 5:
                    coordinates[name] = {
                        'component': row[0],
                        'part': row[1],
                        'x': row[3],
                        'y': row[4],
                        'rotation': row[5],
                        'mount': row[7] if len(row) > 7 else '',
                        'Type': row[8] if len(row) > 8 else '',
                    }
            return {'mash_data': coordinates}
        if isinstance(mash_data, dict) and 'mash_data' in mash_data:
            return mash_data
        return {'mash_data': mash_data}

    @staticmethod
    def recipe_elements(recipe_data):
        if hasattr(recipe_data, 'get_board_components'):
            elements = recipe_data.get_board_components()
        elif isinstance(recipe_data, dict) and 'data' in recipe_data:
            elements = recipe_data['data']['Board']['Children']['a:Element']
        else:
            elements = recipe_data['Board']['Children']['a:Element']
        if isinstance(elements, dict):
            return [elements]
        return elements

    @staticmethod
    def check_if_list_values_in_range(value_list: list, range_value: float, offset: float, threshold: float) ->bool:
        count = 0
        all_val_count = len(value_list)
        result = False
        for value in value_list:
            if range_value - offset <= value <= range_value + offset:
                count += 1
        if count/all_val_count >= threshold:
            result = True
        return result



    @staticmethod
    def calculate_coordinates(x_mash: float, y_mash: float, board_angle: int, part_angle: float, x_mirror=1, y_mirror=1) -> list:
        angle_radians = math.radians(board_angle)
        x = x_mirror * (float(x_mash) * math.cos(angle_radians) - float(y_mash) * math.sin(angle_radians))
        y = y_mirror * (float(x_mash) * math.sin(angle_radians) + float(y_mash) * math.cos(angle_radians))

        results = [x, y, part_angle]

        return results



