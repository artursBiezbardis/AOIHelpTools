from collections import Counter
import math


class ReferenceComponentLocationUtilities:
    ALLOWANCE_OFFSET_X = 0.4
    ALLOWANCE_OFFSET_Y = 0.4
    COLLECT_DIFF_LIMIT = 100
    MASH_BOARD_ANGLES_SEARCH_LIST = [0, 90, 180, 270]
    RESULTS_CONFIDENCE_THRESHOLD = 0.9

    def calculate_statistical_component_angle_diff(self, mash_data: dict, recipe_data: dict):
        angle_differences = []
        for key, component in mash_data.items():
            recipe_component = recipe_data.get(key)
            if recipe_component is None:
                continue
            angle_differences.append(component['angle'] - recipe_component['angle'])
            if len(angle_differences) >= self.COLLECT_DIFF_LIMIT:
                break

        result = Counter(angle_differences)
        return max(result, key=result.get)

    def search_mash_angle_against_recipe(self, mash_data: dict, recipe_data: dict) -> int:
        mash_components = mash_data['mash_data']
        # Parse the shared sample once. Each candidate angle is scored on its own
        # residuals; carrying samples from the previous angle made later rotations
        # both slower and unreliable.
        sample = []
        for element in recipe_data['data']['Board']['Children']['a:Element']:
            component = mash_components.get(element['a:Name'])
            if component is None:
                continue
            location = element['RelativeLocation']
            sample.append((
                float(location['a:X']),
                float(location['a:Y']),
                float(component['x']),
                float(component['y']),
            ))
            if len(sample) >= self.COLLECT_DIFF_LIMIT:
                break

        if not sample:
            return 360

        for angle in self.MASH_BOARD_ANGLES_SEARCH_LIST:
            angle_radians = math.radians(angle)
            cos_angle = math.cos(angle_radians)
            sin_angle = math.sin(angle_radians)
            results_x = []
            results_y = []
            for recipe_x, recipe_y, mash_x, mash_y in sample:
                x_reducer = recipe_x * cos_angle - recipe_y * sin_angle
                y_reducer = recipe_x * sin_angle + recipe_y * cos_angle
                results_x.append(mash_x - x_reducer)
                results_y.append(mash_y - y_reducer)

            x_median = self._median_high(results_x)
            y_median = self._median_high(results_y)
            validate_x = self.check_if_list_values_in_range(
                results_x, x_median, self.ALLOWANCE_OFFSET_X, self.RESULTS_CONFIDENCE_THRESHOLD)
            validate_y = self.check_if_list_values_in_range(
                results_y, y_median, self.ALLOWANCE_OFFSET_Y, self.RESULTS_CONFIDENCE_THRESHOLD)
            if validate_y and validate_x:
                return angle

        return 360

    @staticmethod
    def _median_high(values: list) -> float:
        ordered = sorted(values)
        return ordered[len(ordered) // 2]

    @staticmethod
    def check_if_list_values_in_range(value_list: list, range_value: float, offset: float, threshold: float) -> bool:
        total = len(value_list)
        low = range_value - offset
        high = range_value + offset
        count = 0
        for value in value_list:
            if low <= value <= high:
                count += 1
        return count / total >= threshold


