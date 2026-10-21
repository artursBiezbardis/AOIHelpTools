import unittest

import app.models.mashModels.mashComponentListModel as mash_list_model
import app.repositories.compareRecipeMashRepository.updateBoardComponentsFromMashRepository as update_board
import utilities.referenceComponentLocationUtilities as reference_utilities


def mash_row(name, part='PART-A', x=1.0, y=2.0):
    return [name, part, 'desc', x, y, 0, 'TOP', 'yes', 'SMT', '']


class MashComponentDictTests(unittest.TestCase):

    def test_iteration_uses_component_objects_not_names(self):
        model = mash_list_model.MashComponentListModel({
            'R1': mash_row('R1'),
            'C2': mash_row('C2', 'PART-B', 3.0, 4.0),
        })

        for component in model.component_dict:
            self.assertTrue(hasattr(component, 'get_list'))
            self.assertEqual(component.get_list()[0], component.get_name())

        rebuilt = model.update_mash_model_from_component_dict()
        self.assertEqual(rebuilt['R1'][1], 'PART-A')
        self.assertEqual(rebuilt['C2'][3], 3.0)
        self.assertNotIsInstance(rebuilt['R1'], str)

    def test_string_entries_are_skipped_instead_of_calling_get_list(self):
        model = mash_list_model.MashComponentListModel({'R1': mash_row('R1')})
        model.component_dict['ghost'] = 'R1'
        rebuilt = model.update_mash_model_from_component_dict()
        self.assertIn('R1', rebuilt)
        self.assertNotIn('ghost', rebuilt)

    def test_angle_search_accepts_a_component_model(self):
        model = mash_list_model.MashComponentListModel({
            'R1': mash_row('R1', x=10.0, y=5.0),
        })
        recipe = {
            'data': {
                'Board': {
                    'Children': {
                        'a:Element': {
                            'a:Name': 'R9',
                            'RelativeLocation': {'a:X': '0', 'a:Y': '0'},
                        }
                    }
                }
            }
        }
        result = reference_utilities.ReferenceComponentLocationUtilities().search_mash_angle_against_recipe(
            model,
            recipe,
        )
        self.assertFalse(result['valid'])

    def test_remove_component_missing_from_mash_when_board_has_one_element(self):
        data = {
            'data': {
                'Board': {
                    'Children': {
                        'a:Element': {
                            'a:Name': 'R1',
                            'PartNumber': 'OLD',
                            'RelativeLocation': {'a:X': '1', 'a:Y': '2'},
                        }
                    }
                }
            }
        }
        updated = update_board.UpdateRecipeBoardComponentsFromMashRepository.remove_components(
            data,
            {'R1': {'part': 'empty', 'action': 'remove'}},
        )
        elements = updated['data']['data']['Board']['Children']['a:Element']
        self.assertEqual(elements, [])
        self.assertIn('R1', updated['data']['removed_components'])


if __name__ == '__main__':
    unittest.main()
