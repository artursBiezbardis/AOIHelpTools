from collections import Counter
import math


class ReferenceComponentLocationUtilities:
    ALLOWANCE_OFFSET_X = 0.4
    ALLOWANCE_OFFSET_Y = 0.4
    COLLECT_DIFF_LIMIT = 100
    MASH_BOARD_ANGLES_SEARCH_LIST = [0, 90, 180, 270]
    RESULTS_CONFIDENCE_THRESHOLD = 0.9

    def calculate_statistical_component_angle_diff(self, mash_data: dict, recipe_data: dict):
        count = 0
        angle_differences = []
        for key, component in mash_data.items():
            if key in recipe_data:
                angle_difference: float = component['angle'] - recipe_data[key]['angle']
                angle_differences.append(angle_difference)
                if count >= self.COLLECT_DIFF_LIMIT:
                    break
                count = +1

        result = Counter(angle_differences)
        highest_count_diff_angle = max(result, key=result.get)

        return highest_count_diff_angle

    def search_mash_angle_against_recipe(self, mash_data: dict, recipe_data: dict) -> int:
        result_angle = 360
        results_x = []
        results_y = []
        for angle in self.MASH_BOARD_ANGLES_SEARCH_LIST:
            angle_radians = math.radians(angle)
            count = 1
            for data in recipe_data['data']['Board']['Children']['a:Element']:
                if data['a:Name'] in mash_data['mash_data']:
                    x_reducer = float(data['RelativeLocation']['a:X']) * math.cos(angle_radians) - float(data['RelativeLocation']['a:Y']) * math.sin(angle_radians)
                    y_reducer = float(data['RelativeLocation']['a:X']) * math.sin(angle_radians) + float(data['RelativeLocation']['a:Y']) * math.cos(angle_radians)
                    result_x = float(mash_data['mash_data'][data['a:Name']]['x']) - x_reducer
                    result_y = float(mash_data['mash_data'][data['a:Name']]['y']) - y_reducer
                    results_x.append(result_x)
                    results_y.append(result_y)
                    if count >= self.COLLECT_DIFF_LIMIT:
                        break
                    count = count+1

            x_median = (sorted(results_x))[(len(results_x)) // 2]
            y_median = (sorted(results_y))[(len(results_y)) // 2]
            validate_x = self.check_if_list_values_in_range(results_x, x_median, self.ALLOWANCE_OFFSET_X, self.RESULTS_CONFIDENCE_THRESHOLD)
            validate_y = self.check_if_list_values_in_range(results_y, y_median, self.ALLOWANCE_OFFSET_Y, self.RESULTS_CONFIDENCE_THRESHOLD)
            if validate_y and validate_x:
                result_angle = angle
                break

        return result_angle

    @staticmethod
    def check_if_list_values_in_range(value_list: list, range_value: float, offset: float, threshold: float) ->bool:
        count = 0
        all_val_count = len(value_list)
        result = False
        for value in value_list:
            if range_value - offset <= value <= range_value + offset:
                count = count + 1
        if count/all_val_count >= threshold:
            result = True
        return result


