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
                count += 1
                if count >= self.COLLECT_DIFF_LIMIT:
                    break

        result = Counter(angle_differences)
        highest_count_diff_angle = max(result, key=result.get)

        return highest_count_diff_angle

    def search_mash_angle_against_recipe(self, mash_data: dict, recipe_data: dict) -> int:
        samples = self._matching_samples(mash_data, recipe_data)
        if not samples:
            return 360
        for angle in self.MASH_BOARD_ANGLES_SEARCH_LIST:
            angle_radians = math.radians(angle)
            cosine = math.cos(angle_radians)
            sine = math.sin(angle_radians)
            results_x = []
            results_y = []
            for recipe_x, recipe_y, mash_x, mash_y in samples:
                x_reducer = recipe_x * cosine - recipe_y * sine
                y_reducer = recipe_x * sine + recipe_y * cosine
                results_x.append(mash_x - x_reducer)
                results_y.append(mash_y - y_reducer)
            x_median = sorted(results_x)[len(results_x) // 2]
            y_median = sorted(results_y)[len(results_y) // 2]
            validate_x = self.check_if_list_values_in_range(
                results_x, x_median, self.ALLOWANCE_OFFSET_X, self.RESULTS_CONFIDENCE_THRESHOLD
            )
            validate_y = self.check_if_list_values_in_range(
                results_y, y_median, self.ALLOWANCE_OFFSET_Y, self.RESULTS_CONFIDENCE_THRESHOLD
            )
            if validate_y and validate_x:
                return angle

        return 360

    def _matching_samples(self, mash_data, recipe_data):
        mash = mash_data['mash_data']
        elements = recipe_data['data']['Board']['Children']['a:Element']
        if isinstance(elements, dict):
            elements = [elements]
        samples = []
        limit = self.COLLECT_DIFF_LIMIT
        for element in elements:
            if not isinstance(element, dict):
                continue
            name = element.get('a:Name')
            if name not in mash:
                continue
            location = element['RelativeLocation']
            component = mash[name]
            samples.append((
                float(location['a:X']),
                float(location['a:Y']),
                float(component['x']),
                float(component['y']),
            ))
            if len(samples) >= limit:
                break
        return samples

    @staticmethod
    def check_if_list_values_in_range(value_list: list, range_value: float, offset: float, threshold: float) -> bool:
        all_val_count = len(value_list)
        if all_val_count == 0:
            return False
        needed = threshold * all_val_count
        count = 0
        low = range_value - offset
        high = range_value + offset
        for index, value in enumerate(value_list):
            if low <= value <= high:
                count += 1
                if count >= needed:
                    return True
            elif count + (all_val_count - index - 1) < needed:
                return False
        return False
