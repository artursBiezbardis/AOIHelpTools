import utilities.recipeProcessUtilities as recipeProcess
import app.repositories.compareRecipeMashRepository.updateBoardComponentsFromMashRepository as updateBoard
import app.repositories.compareRecipeMashRepository.setUpdatedPartsToSharedRepository as updatePanel
import utilities.backUpUtilities as recipeBackUp
import os
import helpers.helpers as helper


class UpdateRecipeComponentsFromMash:

    def main(self, table: list, recipe_path: str, actions: dict):

        recipe_process = recipeProcess.RecipeProcessUtilities()
        helpers = helper.Helpers()
        recipe_gzip_files = recipe_process.prepare_tmp_recipe_data(recipe_path)
        update_dictionary = self.get_components_for_update(table[0], actions.get('ADD_COMPONENTS'))
        self.update_recipe_boards(recipe_gzip_files, update_dictionary, table[1], actions)
        parts_list = self.get_part_list(update_dictionary)
        updatePanel.SetUpdatedPartsToSharedRepository().main(parts_list, recipe_gzip_files['gzip_extract_path']+'/Panel')
        backup_dir = os.path.dirname(recipe_path)+'/backupRecipes'
        recipeBackUp.BackUpUtilities.create_backup_for_file(backup_dir, recipe_path, 'recipe_before_update_from_mash_')
        list_of_gzip_files = helpers.get_files_in_folder(recipe_gzip_files['gzip_extract_path'])
        recipe_process.create_recipe_from_tmp(recipe_path, list_of_gzip_files)

    @staticmethod
    def _difference_rows(table):
        for item in table or []:
            if item and item[0] != 'All components validated!!':
                yield item

    @classmethod
    def validate_table_for_update(cls, table=None):
        for component in cls._difference_rows(table):
            if len(component) > 1 and component[1] != 'empty':
                return True
        return False

    @classmethod
    def table_has_components_to_add(cls, table=None):
        for component in cls._difference_rows(table):
            if len(component) > 2 and component[1] == 'empty' and component[2] not in ('empty', ''):
                return True
        return False

    @classmethod
    def update_is_available(cls, table, add_selected) -> bool:
        return cls.validate_table_for_update(table) or (bool(add_selected) and cls.table_has_components_to_add(table))

    @classmethod
    def get_components_for_update(cls, table: list, add_components=False) -> dict:
        components_to_update = {}
        for item in cls._difference_rows(table):
            if len(item) < 3:
                continue
            if item[1] != 'empty' and item[2] != 'empty':
                components_to_update[item[0]] = item[2]
            elif item[1] != 'empty' and item[2] == 'empty':
                components_to_update[item[0]] = 'remove'
            elif add_components and item[1] == 'empty' and item[2] not in ('empty', ''):
                components_to_update[item[0]] = item[2]
        return components_to_update

    @staticmethod
    def update_recipe_boards(recipe_gzip_files, update_dictionary, mash_data, actions):
        boards_list_gzip = recipe_gzip_files['gzip_list']
        boards_list_gzip.remove('Panel')
        for board_file in boards_list_gzip:
            board_path = recipe_gzip_files['gzip_extract_path']+'/'+board_file
            updateBoard.UpdateRecipeBoardComponentsFromMashRepository()\
                .update_board_components(board_path, update_dictionary, mash_data, actions)

    def set_parts_to_shared(self, update_dictionary):
        part_list = self.get_part_list(update_dictionary)

        return part_list

    @staticmethod
    def get_part_list(update_dictionary):
        part_list = []
        for _key, val in update_dictionary.items():
            if val and val != 'remove' and val not in part_list:
                part_list.append(val)

        return part_list
