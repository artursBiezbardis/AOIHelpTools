import gzip
import io
import json
import math
import os
import sqlite3
import sys
import tempfile
import types
import unittest
import xmltodict
from contextlib import redirect_stdout
from unittest.mock import patch

sys.modules.setdefault('PySimpleGUI', types.ModuleType('PySimpleGUI'))

import app.models.LocationsCollection as locations_collection
import app.models.areaLocationModel as area_location_model
import app.repositories.groupComponentsByLocationRepository.areaLocationRepository as area_location_repository
import app.repositories.groupComponentsByLocationRepository.updateRecipeComponentsRepository as update_recipe_repository
import app.repositories.recipesListRepository.recipesListRepository as recipes_list_repository
import app.repositories.sqlLiteRepository.sqlLiteRepository as sqlite_repository
import app.services.compareRecipeMashServices.compareRecipeMashService as compare_recipe_service
import app.services.mashFileServices.mashFileService as mash_service
import app.services.recipesListService.recipesListService as recipes_list_service
import app.services.recipesListService.updateRecipesService as update_recipes_service
import app.services.settingsService.settingsService as settings_service
import helpers.compressAndExtractRecipesHelper as compress_helper
import helpers.helpers as helpers_module
import helpers.viewHelpers as view_helpers


class HelperTests(unittest.TestCase):

    def setUp(self):
        self.helpers = helpers_module.Helpers()

    def test_replace_special_letters_matches_the_latvian_map(self):
        mapping = {
            'ā': 'a', 'ē': 'e', 'ī': 'i', 'ū': 'u',
            'Ā': 'A', 'Ē': 'E', 'Ī': 'I', 'Ū': 'U',
            'č': 'c', 'ģ': 'g', 'ķ': 'k', 'ļ': 'l', 'ņ': 'n', 'š': 's', 'ž': 'z',
            'Č': 'C', 'Ģ': 'G', 'Ķ': 'K', 'Ļ': 'L', 'Ņ': 'N', 'Š': 'S', 'Ž': 'Z',
        }
        self.assertEqual(
            self.helpers.replace_special_letters(''.join(mapping)),
            ''.join(mapping.values()),
        )
        self.assertEqual(self.helpers.replace_special_letters('Cģ-123'), 'Cg-123')
        self.assertEqual(self.helpers.replace_special_letters('ABC'), 'ABC')

    def test_is_number_matches_float(self):
        corpus = [
            '1_000', ' 1 ', '\n1\t', 'nan', 'NaN', '+inf', '-Infinity', '1e-3', '1,2', '',
            'abc', 'TYPE', 'FAN', 'RESISTOR', 'ā', '٠١', '１', 'Infinity', 'InFiNiTy',
            '+NaN', 'sNaN', '1e', '0e0', '  nan  ', '\u00a01', '1.2.3', '+.5', '-.5',
            'ž', '100nF', '10uF', '--1', 'e', 'E10', '0', '00',
        ]
        for value in corpus:
            try:
                float(value)
                expected = True
            except ValueError:
                expected = False
            self.assertEqual(self.helpers.is_number(value), expected, value)

        for value in (0, 1.5, True, False, float('nan'), float('inf')):
            self.assertTrue(self.helpers.is_number(value))
        with self.assertRaises(TypeError):
            self.helpers.is_number(None)

    def test_string_padding_matches_ljust(self):
        view = view_helpers.ViewHelper()
        self.assertEqual(view.string_length_adjustment_with_white_space('ab', 5), 'ab   ')
        self.assertEqual(view.string_length_adjustment_with_white_space('ab', 5, 'c'), 'abc  ')
        self.assertEqual(view.string_length_adjustment_with_white_space('abcdef', 3), 'abcdef')


class MashServiceTests(unittest.TestCase):

    def test_component_names(self):
        valid = mash_service.MashFileService.is_valid_component_name
        self.assertTrue(valid('R1'))
        self.assertTrue(valid('C1234567'))
        self.assertFalse(valid('R12345678'))
        self.assertFalse(valid('R'))
        self.assertFalse(valid('123'))
        self.assertFalse(valid('R1A'))
        self.assertFalse(valid(None))
        self.assertFalse(valid(12))

    def test_rows_differ_matches_json(self):
        samples = [
            1, 1.0, True, False, None, 'A', '',
            float('nan'), float('inf'), float('-inf'), 0.0, -0.0, '1', 10,
        ]
        differ = mash_service.MashFileService.rows_differ
        for left in samples:
            for right in samples:
                row_left = [left]
                row_right = [right]
                self.assertEqual(
                    differ(row_left, row_right),
                    json.dumps(row_left) != json.dumps(row_right),
                    msg=(left, right),
                )
        self.assertTrue(differ([1], [1, 2]))
        self.assertFalse(differ([float('nan'), 'A'], [float('nan'), 'A']))

    def test_format_data_content(self):
        formatted = mash_service.MashFileService.format_data_content(
            [True, '1,5', 'ā', float('nan'), None, 'inf', 'TYPE', ' 12 ', 'x', 'y', 'EXTRA']
        )
        self.assertEqual(len(formatted), 10)
        self.assertIs(formatted[0], True)
        self.assertEqual(formatted[1], 1.5)
        self.assertEqual(formatted[2], 'A')
        self.assertTrue(math.isnan(formatted[3]))
        self.assertEqual(formatted[4], 'NONE')
        self.assertEqual(formatted[5], float('inf'))
        self.assertEqual(formatted[6], 'TYPE')
        self.assertEqual(formatted[7], 12.0)
        self.assertEqual(formatted[8], 'X')
        self.assertEqual(formatted[9], 'Y')

    def test_component_list_does_not_mutate_inputs(self):
        left = ['R2', 'R1', 'R1']
        right = ['C1', 'R2']
        original_left = list(left)
        names = mash_service.MashFileService.get_list_of_components_from_mashes(left, right)
        self.assertEqual(names, ['C1', 'R1', 'R2'])
        self.assertEqual(left, original_left)

    def test_compare_two_mashes(self):
        rows_a = [
            ['Designator', 'Part', 'Desc', 'X', 'Y', 'Rot', 'Side', 'Mount', 'Type', 'Remarks'],
            ['R1', 'aaa', 'žā', 1, 2, 3, 'top', 'yes', 'smd', 'note', 'IGNORE'],
            ['R2', 'same', 'd', 1.0, 2.0, 3.0, 'top', 'yes', 'smd', 'n'],
        ]
        rows_b = [
            ['Designator', 'Part', 'Desc', 'X', 'Y', 'Rot', 'Side', 'Mount', 'Type', 'Remarks'],
            ['R1', 'bbb', 'ža', 1, 2, 3, 'top', 'yes', 'smd', 'note'],
            ['C10', 'onlyb', 'd', 1, 2, 3, 'bot', 'yes', 'smd', 'n'],
        ]
        flags = {
            '-PART_NUMBER-': True,
            '-DESCRIPTION-': True,
            '-X_CORD-': True,
            '-Y_CORD-': True,
            '-ROTATION-': True,
            '-SIDE-': True,
        }

        def tables(location):
            source = rows_a if location.endswith('a.xlsx') else rows_b
            return [list(row) for row in source]

        service = mash_service.MashFileService()
        with patch(
            'app.services.mashFileServices.mashFileService.mashFileRepo.MashFileRepository.get_mash_table',
            side_effect=tables,
        ):
            table, diffs = service.compare_two_mashes('a.xlsx', 'b.xlsx', flags)

        self.assertEqual(len(table), 9)
        self.assertEqual(table[0][0], 'a.xlsx')
        self.assertEqual(table[0][1], 'no data')
        self.assertEqual(table[1][0], 'b.xlsx')
        self.assertEqual(table[1][1], 'C10')
        self.assertEqual(table[1][2], 'ONLYB')
        self.assertEqual(table[3][1], 'R1')
        self.assertEqual(table[3][2], 'AAA')
        self.assertEqual(table[3][3], 'ZA')
        self.assertEqual(table[4][2], 'BBB')
        self.assertEqual(table[4][3], 'ZA')
        self.assertEqual(diffs[2], [4, 1])
        self.assertEqual(diffs[3], [5, 1])

        ignored = dict(flags)
        ignored['-PART_NUMBER-'] = False
        with patch(
            'app.services.mashFileServices.mashFileService.mashFileRepo.MashFileRepository.get_mash_table',
            side_effect=tables,
        ):
            table, _diffs = service.compare_two_mashes('a.xlsx', 'b.xlsx', ignored)
        self.assertFalse(any(row and row[1] == 'R1' for row in table))

    def test_locate_diff_treats_nan_as_different_cells(self):
        diff1, diff2 = mash_service.MashFileService.locate_diff_in_row(
            3,
            [1.0, float('nan')],
            [1.0, float('nan')],
        )
        self.assertEqual(diff1, [3, 1])
        self.assertEqual(diff2, [4, 1])


class BoardSideTests(unittest.TestCase):

    def row(self, part='PART', side='TOP', mount='yes', comp_type='SMD'):
        return ['COMP', part, '', 0, 0, 0, side, mount, comp_type, '']

    def test_filters_side_tht_and_unmounted_parts(self):
        service = compare_recipe_service.CompareRecipeMashService
        mash = [
            'file',
            [],
            {
                'R1': self.row(part=' abc ', side='BOTTOM'),
                'R2': self.row(side='TOP'),
                'R3': self.row(comp_type='THT', mount=1.5),
                'R4': self.row(mount='NO'),
                'R5': self.row(mount='nm'),
                'R6': self.row(part=float('nan')),
                'R7': self.row(comp_type=float('nan')),
                'R8': ['COMP', 'P', '', 0, 0, 0, float('nan')],
            },
        ]
        selected = service.get_board_side_data(mash, 'bot')
        self.assertEqual(list(selected), ['R1'])
        self.assertEqual(selected['R1']['part'], 'abc')
        self.assertEqual(selected['R1']['Type'], 'SMD')
        self.assertEqual(selected['R1']['mount'], 'yes')

        del mash[2]['R8']
        everything = service.get_board_side_data(mash, 'no_side')
        self.assertEqual(list(everything), ['R1', 'R2'])


class RecipeCompareTests(unittest.TestCase):

    def write_board(self, directory, elements):
        os.makedirs(os.path.join(directory, 'tmp'))
        xml = xmltodict.unparse({'Board': {'Children': {'a:Element': elements}}})
        with gzip.open(os.path.join(directory, 'tmp', '0.board'), 'wb') as board:
            board.write(xml.encode('utf-8'))

    def test_reports_part_mismatches_and_missing_components(self):
        elements = [
            {'a:Name': 'R1', 'PartNumber': 'XXABC'},
            {'a:Name': 'R2', 'PartNumber': 'OTHER'},
            {'a:Name': 'R3', 'PartNumber': 'SOMEPART'},
            {'a:Name': 'R4', 'PartNumber': 'Template_FOD'},
            {'a:Name': 'R5', 'PartNumber': 'ONLYRECIPE'},
        ]
        mash = {
            'R1': {'part': 'ABC', 'mount': 'yes', 'Type': 'SMD'},
            'R2': {'part': 'DIFF', 'mount': 'yes', 'Type': 'SMD'},
            'C9': {'part': 'ONLYMASH', 'mount': 'no', 'Type': 'SMT'},
        }
        with tempfile.TemporaryDirectory() as directory:
            self.write_board(directory, elements)
            table = compare_recipe_service.CompareRecipeMashService.compare_recipe_to_mash(
                directory,
                mash,
            )
            self.assertFalse(os.path.exists(os.path.join(directory, 'tmp')))
        self.assertEqual(table, [
            ['R2', 'OTHER', 'DIFF', 'yes', 'SMD'],
            ['R5', 'ONLYRECIPE', 'empty', 'empty', 'empty'],
            ['C9', 'empty', 'ONLYMASH', 'no', 'SMT'],
        ])
        self.assertEqual(list(mash), ['C9'])

    def test_all_components_validated(self):
        elements = [
            {'a:Name': 'R1', 'PartNumber': 'ABC'},
            {'a:Name': 'R2', 'PartNumber': 'DEF'},
        ]
        mash = {
            'R1': {'part': 'ABC', 'mount': 'yes', 'Type': 'SMD'},
            'R2': {'part': 'DEF', 'mount': 'yes', 'Type': 'SMD'},
        }
        with tempfile.TemporaryDirectory() as directory:
            self.write_board(directory, elements)
            table = compare_recipe_service.CompareRecipeMashService.compare_recipe_to_mash(
                directory,
                mash,
            )
        self.assertEqual(table, [[
            'All components validated!!',
            'All components validated!!',
            'All components validated!!',
        ]])


class SqliteAndRecipeSearchTests(unittest.TestCase):

    def create_component_db(self, path, rows):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        connection = sqlite3.connect(path)
        connection.execute(
            'CREATE TABLE Component (TemplateId TEXT, packageName TEXT, data BLOB)'
        )
        connection.executemany(
            'INSERT INTO Component (TemplateId, packageName, data) VALUES (?, ?, ?)',
            rows,
        )
        connection.commit()
        connection.close()

    def test_repository_reads_value_column_and_limits_existence_check(self):
        repository = sqlite_repository.SQLiteRepository()
        with tempfile.TemporaryDirectory() as directory:
            settings_db = os.path.join(directory, 'settings.db')
            connection = sqlite3.connect(settings_db)
            connection.execute('CREATE TABLE setup (Name TEXT, Value TEXT)')
            connection.execute("INSERT INTO setup VALUES ('-RECIPES_PATH-', 'Z:/Recipe')")
            connection.commit()
            connection.close()
            self.assertEqual(
                repository.read_value_by_name('setup', '-RECIPES_PATH-', settings_db),
                'Z:/Recipe',
            )

            component_db = os.path.join(directory, 'templates.db')
            blob = b'x' * 1000
            self.create_component_db(component_db, [
                ('ABC', 'PKG1', blob),
                ('ZZZ', 'PKG2', blob),
            ])
            self.assertTrue(repository.check_if_entry_exist('Component', 'TemplateId', 'ABC', component_db))
            self.assertFalse(repository.check_if_entry_exist('Component', 'TemplateId', 'MISSING', component_db))
            self.assertEqual(repository.get_component_package_name('Component', 'ABC', component_db), ('PKG1',))
            self.assertEqual(
                repository.lookup_component_package('Component', 'TemplateId', 'abc', component_db),
                (False, None),
            )
            self.assertEqual(
                repository.lookup_component_package('Component', 'TemplateId', 'ABC', component_db),
                (True, 'PKG1'),
            )
            with self.assertRaises(TypeError):
                repository.lookup_component_package('Component', 'PackageName', 'PKG2', component_db)

    def test_package_lookup_still_uses_template_id(self):
        repository = sqlite_repository.SQLiteRepository()
        with tempfile.TemporaryDirectory() as directory:
            component_db = os.path.join(directory, 'templates.db')
            self.create_component_db(component_db, [
                ('SOIC', 'SOIC', b''),
            ])
            self.assertEqual(
                repository.lookup_component_package('Component', 'PackageName', 'SOIC', component_db),
                (True, 'SOIC'),
            )
            self.assertEqual(
                repository.lookup_component_package('Component', 'PackageName', 'QFN', component_db),
                (False, None),
            )
            self.create_component_db(os.path.join(directory, 'missing-package.db'), [
                ('OTHER', 'QFN', b''),
            ])
            with self.assertRaises(TypeError):
                repository.lookup_component_package(
                    'Component',
                    'PackageName',
                    'QFN',
                    os.path.join(directory, 'missing-package.db'),
                )

    def test_find_recipes_preserves_directory_order(self):
        suffix = recipes_list_service.RecipesListService.dBSubLocation
        with tempfile.TemporaryDirectory() as directory:
            blob = os.urandom(64)
            matching = []
            for name, template_id, package_name in (
                ('recipe-b', 'ZZZ', 'NO'),
                ('recipe-a', 'ABC', 'PKG1'),
                ('recipe-c', 'ABC', None),
            ):
                recipe_path = os.path.join(directory, name)
                os.makedirs(recipe_path)
                self.create_component_db(recipe_path + suffix, [(template_id, package_name, blob)])
                if template_id == 'ABC':
                    matching.append(name)

            service = recipes_list_service.RecipesListService()
            with patch(
                'app.services.recipesListService.recipesListService.settings.SettingsService.get_setting',
                return_value=directory,
            ):
                found = service.format_list_for_table('abc', 'Component')
                directories = recipes_list_repository.RecipesListRepository.folder_dict(directory)
            expected_order = [name for name in directories if name in matching]
            self.assertEqual(list(found), expected_order)
            self.assertEqual(found['recipe-a']['Package'], 'PKG1')
            self.assertIsNone(found['recipe-c']['Package'])
            self.assertEqual(found['recipe-a']['location'], os.path.join(directory, 'recipe-a'))
            self.assertNotIn('recipe-b', found)

            single_root = tempfile.TemporaryDirectory()
            self.addCleanup(single_root.cleanup)
            single_recipe = os.path.join(single_root.name, 'solo')
            os.makedirs(single_recipe)
            self.create_component_db(single_recipe + suffix, [('ABC', 'SOLO', b'')])
            with patch(
                'app.services.recipesListService.recipesListService.settings.SettingsService.get_setting',
                return_value=single_root.name,
            ):
                solo = service.format_list_for_table('ABC', 'Component')
            self.assertEqual(list(solo), ['solo'])
            self.assertEqual(solo['solo']['Package'], 'SOLO')

    def test_folder_dict_skips_files(self):
        with tempfile.TemporaryDirectory() as directory:
            os.makedirs(os.path.join(directory, 'recipe'))
            with open(os.path.join(directory, 'note.txt'), 'w', encoding='utf-8') as handle:
                handle.write('x')
            found = recipes_list_repository.RecipesListRepository.folder_dict(directory)
            self.assertEqual(list(found), ['recipe'])
            self.assertEqual(found['recipe'], os.path.join(directory, 'recipe'))

    def test_settings_update_uses_one_transaction(self):
        with tempfile.TemporaryDirectory() as directory:
            database = os.path.join(directory, 'settings.db')
            connection = sqlite3.connect(database)
            connection.execute('CREATE TABLE setup (Name TEXT, Value TEXT)')
            connection.executemany(
                'INSERT INTO setup VALUES (?, ?)',
                [('-RECIPES_PATH-', 'old-recipes'), ('-LIBRARY_PATH-', 'old-library')],
            )
            connection.commit()
            connection.close()

            service = settings_service.SettingsService()
            service.data_base = database
            service.update_settings_values({
                '-RECIPES_PATH-': 'old-recipes',
                '-LIBRARY_PATH-': 'new-library',
            })
            connection = sqlite3.connect(database)
            rows = dict(connection.execute('SELECT Name, Value FROM setup'))
            connection.close()
            self.assertEqual(rows['-RECIPES_PATH-'], 'old-recipes')
            self.assertEqual(rows['-LIBRARY_PATH-'], 'new-library')


class RecipeUpdateTests(unittest.TestCase):

    def test_update_extracts_each_recipe_once(self):
        service = update_recipes_service.UpdateRecipesService()
        recipes = {
            'a': {'location': '/data/recipe-a', 'Package': 'PKG'},
            'b': {'location': '/data/recipe-b', 'Package': 'PKG'},
        }
        with patch.object(
            update_recipes_service.UpdateRecipesService,
            'prepare_recipe_data',
            return_value=['Panel'],
        ) as prepare, patch(
            'app.services.recipesListService.updateRecipesService.updateRecipesRepository.UpdateRecipesRepository.stream_gzip_for_update'
        ), patch.object(
            update_recipes_service.UpdateRecipesService,
            'create_backup_for_file',
        ), patch(
            'app.services.recipesListService.updateRecipesService.compressAndExtractRecipes.CompressAndExtractRecipesHelper.compress_files_zip'
        ), patch(
            'app.services.recipesListService.updateRecipesService.shutil.rmtree'
        ) as remove_tree:
            service.update_recipes(recipes, 'PART', 'Component')
        self.assertEqual(prepare.call_count, 2)
        self.assertEqual(remove_tree.call_count, 2)


class AreaAndArchiveTests(unittest.TestCase):

    def test_area_bounds_are_inclusive(self):
        area = area_location_model.AreaLocation(
            location_name='a',
            x=10,
            y=10,
            width=4,
            height=6,
            offset_x=99,
            offset_y=99,
            left_line_offset=-1,
            right_line_offset=0.5,
            up_line_offset=1,
            down_line_offset=-0.5,
        )
        self.assertTrue(area.check_contains_component(7, 6.5))
        self.assertTrue(area.check_contains_component(12.5, 14))
        self.assertFalse(area.check_contains_component(6.9, 10))
        self.assertFalse(area.check_contains_component(10, 14.1))

    def test_area_repository_parses_offsets_for_one_or_many_elements(self):
        area_location_repository.AreaLocationRepository.area_location_collection = (
            locations_collection.LocationsData([])
        )
        view_input = {
            '-X_OFFSET-': '1.5',
            '-Y_OFFSET-': '2',
            '-LEFT_OFFSET-': '0',
            '-RIGHT_OFFSET-': '0',
            '-UP_OFFSET-': '0',
            '-DOWN_OFFSET-': '0',
        }
        elements = [
            {
                'a:Name': 'A1',
                'RelativeLocation': {'a:X': '1', 'a:Y': '2'},
                'Bodies': {'a:Body': {'a:Shape': {'Height': '3', 'Base': '4'}}},
            },
            {
                'a:Name': 'A2',
                'RelativeLocation': {'a:X': '5', 'a:Y': '6'},
                'Bodies': {'a:Body': {'a:Shape': {'Height': '7', 'Base': '8'}}},
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            many_path = os.path.join(directory, 'many.xml')
            with open(many_path, 'w', encoding='utf-8') as handle:
                handle.write(xmltodict.unparse({'Board': {'Children': {'a:Element': elements}}}))
            one_path = os.path.join(directory, 'one.xml')
            with open(one_path, 'w', encoding='utf-8') as handle:
                handle.write(xmltodict.unparse({'Board': {'Children': {'a:Element': elements[0]}}}))
            repository = area_location_repository.AreaLocationRepository()
            many = repository.get_area_location_data(many_path, view_input).get_location_collection()
            self.assertEqual([item.location_name for item in many], ['A1', 'A2'])
            self.assertEqual(many[0].offset_x, 1.5)
            self.assertEqual(many[0].width, 4)
            one = repository.get_area_location_data(one_path, view_input).get_location_collection()
            self.assertEqual([item.location_name for item in one], ['A1', 'A2', 'A1'])

    def test_grouped_components_inside_an_area_get_the_suffix(self):
        area = area_location_model.AreaLocation(
            location_name='box',
            x=0,
            y=0,
            width=2,
            height=2,
            offset_x=0,
            offset_y=0,
            left_line_offset=0,
            right_line_offset=0,
            up_line_offset=0,
            down_line_offset=0,
        )
        elements = [
            {
                'a:Name': 'T1',
                'RelativeLocation': {'a:X': '0', 'a:Y': '0'},
                'a:TemplateName': 'TPL',
                'PackageName': 'PKG',
                'PartNumber': 'PART',
            },
            {
                'a:Name': 'R1',
                'RelativeLocation': {'a:X': '0', 'a:Y': '0'},
                'a:TemplateName': 'TPL',
                'PackageName': 'PKG',
                'PartNumber': 'PART',
            },
            {
                'a:Name': 'R2',
                'RelativeLocation': {'a:X': '20', 'a:Y': '20'},
                'a:TemplateName': 'TPL',
                'PackageName': 'PKG',
                'PartNumber': 'PART',
            },
            {'a:Name': None},
        ]
        xml = xmltodict.unparse({'Board': {'Children': {'a:Element': elements}}}).encode('utf-8')
        source = io.BytesIO()
        with gzip.GzipFile(fileobj=source, mode='wb') as handle:
            handle.write(xml)
        source.seek(0)
        with redirect_stdout(io.StringIO()):
            updated = update_recipe_repository.UpdateRecipeComponentsRepository. \
                update_board_components_in_selected_areas_gzip_stream(source, [area], '_G')
        with gzip.GzipFile(fileobj=updated, mode='rb') as handle:
            data = xmltodict.parse(handle.read())
        names = {
            element['a:Name']: element
            for element in data['Board']['Children']['a:Element']
            if isinstance(element, dict) and element.get('a:Name')
        }
        self.assertEqual(names['T1']['PartNumber'], 'PART')
        self.assertEqual(names['R1']['PartNumber'], 'PART_G')
        self.assertEqual(names['R1']['PackageName'], 'PKG_G')
        self.assertEqual(names['R1']['a:TemplateName'], 'TPL_G')
        self.assertEqual(names['R2']['PartNumber'], 'PART')

    def test_gzip_round_trip_streams_the_same_bytes(self):
        payload = b'board-xml' * 1000
        with tempfile.TemporaryDirectory() as directory:
            source_name = 'board.xml'
            with open(os.path.join(directory, source_name), 'wb') as handle:
                handle.write(payload)
            compressed = os.path.join(directory, 'board.gz')
            compress_helper.CompressAndExtractRecipesHelper.compress_gzip(directory + os.sep, source_name, compressed)
            extracted = os.path.join(directory, 'out.xml')
            relative_out = 'out.xml'
            compress_helper.CompressAndExtractRecipesHelper.extract_gzip(directory + os.sep, 'board.gz', relative_out)
            with open(extracted, 'rb') as handle:
                self.assertEqual(handle.read(), payload)


if __name__ == '__main__':
    unittest.main()
