from collections import Counter
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class BoardTransform:
    """How one recipe board sits in mash coordinates.

    mash_xy = rotate(mirror(recipe_xy), angle) + offset
    recipe rotation = rotation_sign * mash rotation + rotation_delta
    """

    angle: int = 360
    mirror_x: bool = False
    mirror_y: bool = False
    offset_x: float = 0.0
    offset_y: float = 0.0
    rotation_sign: int = 1
    rotation_delta: int = 0

    @property
    def found(self) -> bool:
        return self.angle != 360


class ReferenceComponentLocationUtilities:
    ALLOWANCE_OFFSET_X = 0.4
    ALLOWANCE_OFFSET_Y = 0.4
    COLLECT_DIFF_LIMIT = 100
    MIN_REFERENCE_COMPONENTS = 3
    MASH_BOARD_ANGLES_SEARCH_LIST = [0, 90, 180, 270]
    # Mirroring Y and then rotating is the same placement as mirroring X and rotating
    # an extra 180 degrees, so one mirror axis covers both.
    MIRROR_OPTIONS = ((False, False), (True, False))
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
        return self.find_board_transform(mash_data, recipe_data).angle

    def find_board_transform(self, mash_data: dict, recipe_data: dict) -> BoardTransform:
        mash_components = mash_data['mash_data']
        elements = recipe_data['data']['Board']['Children']['a:Element']
        # One shared sample. Each candidate is scored on its own residuals so a
        # later rotation or mirror is not judged on points from the previous try.
        sample = []
        for element in self.as_element_list(elements):
            try:
                component = mash_components.get(str(element['a:Name']).strip())
                if component is None:
                    continue
                location = element['RelativeLocation']
                recipe_rotation = self._optional_rotation(element.get('RelativeRotation'))
                mash_rotation = self._optional_rotation(component.get('rotation'))
                sample.append((
                    float(location['a:X']),
                    float(location['a:Y']),
                    float(component['x']),
                    float(component['y']),
                    mash_rotation,
                    recipe_rotation,
                ))
            except (TypeError, KeyError, ValueError):
                continue
            if len(sample) >= self.COLLECT_DIFF_LIMIT:
                break

        if len(sample) < self.MIN_REFERENCE_COMPONENTS:
            return BoardTransform()

        for mirror_x, mirror_y in self.MIRROR_OPTIONS:
            for angle in self.MASH_BOARD_ANGLES_SEARCH_LIST:
                transform = self._fit_transform(sample, angle, mirror_x, mirror_y)
                if transform is not None:
                    return transform

        return BoardTransform()

    def mash_to_recipe_position(self, transform: BoardTransform, mash_x: float, mash_y: float):
        radians = math.radians(transform.angle)
        cos_angle = math.cos(radians)
        sin_angle = math.sin(radians)
        dx = float(mash_x) - transform.offset_x
        dy = float(mash_y) - transform.offset_y
        recipe_x = dx * cos_angle + dy * sin_angle
        recipe_y = -dx * sin_angle + dy * cos_angle
        if transform.mirror_x:
            recipe_x = -recipe_x
        if transform.mirror_y:
            recipe_y = -recipe_y
        return recipe_x, recipe_y

    def mash_to_recipe_rotation(self, transform: BoardTransform, mash_rotation) -> int:
        return self.normalize_deg(transform.rotation_sign * float(mash_rotation) + transform.rotation_delta)

    def _fit_transform(self, sample, angle, mirror_x, mirror_y):
        radians = math.radians(angle)
        cos_angle = math.cos(radians)
        sin_angle = math.sin(radians)
        results_x = []
        results_y = []
        for recipe_x, recipe_y, mash_x, mash_y, _mash_rotation, _recipe_rotation in sample:
            mirrored_x = -recipe_x if mirror_x else recipe_x
            mirrored_y = -recipe_y if mirror_y else recipe_y
            mapped_x = mirrored_x * cos_angle - mirrored_y * sin_angle
            mapped_y = mirrored_x * sin_angle + mirrored_y * cos_angle
            results_x.append(mash_x - mapped_x)
            results_y.append(mash_y - mapped_y)

        offset_x = self._median_high(results_x)
        offset_y = self._median_high(results_y)
        if not self.check_if_list_values_in_range(
            results_x, offset_x, self.ALLOWANCE_OFFSET_X, self.RESULTS_CONFIDENCE_THRESHOLD
        ):
            return None
        if not self.check_if_list_values_in_range(
            results_y, offset_y, self.ALLOWANCE_OFFSET_Y, self.RESULTS_CONFIDENCE_THRESHOLD
        ):
            return None

        rotation_sign, rotation_delta = self._fit_rotation(sample, angle, mirror_x, mirror_y)
        return BoardTransform(
            angle=angle,
            mirror_x=mirror_x,
            mirror_y=mirror_y,
            offset_x=offset_x,
            offset_y=offset_y,
            rotation_sign=rotation_sign,
            rotation_delta=rotation_delta,
        )

    def _fit_rotation(self, sample, angle, mirror_x, mirror_y):
        pairs = [
            (mash_rotation, recipe_rotation)
            for _recipe_x, _recipe_y, _mash_x, _mash_y, mash_rotation, recipe_rotation in sample
            if mash_rotation is not None and recipe_rotation is not None
        ]
        mirrored = mirror_x or mirror_y
        if not pairs:
            sign = -1 if mirrored else 1
            delta = angle if mirrored else self.normalize_deg(-angle)
            return sign, delta

        best_sign = -1 if mirrored else 1
        best_delta = 0
        best_count = -1
        for sign in (1, -1):
            deltas = [self.normalize_deg(recipe_rotation - sign * mash_rotation) for mash_rotation, recipe_rotation in pairs]
            delta, count = Counter(deltas).most_common(1)[0]
            if count > best_count:
                best_sign = sign
                best_delta = delta
                best_count = count
        return best_sign, best_delta

    @staticmethod
    def as_element_list(elements):
        if isinstance(elements, list):
            return elements
        if isinstance(elements, dict):
            return [elements]
        return []

    @staticmethod
    def _optional_rotation(value):
        if value is None:
            return None
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        if math.isnan(number) or math.isinf(number):
            return None
        return number

    @staticmethod
    def normalize_deg(value) -> int:
        return int(round(float(value))) % 360

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


