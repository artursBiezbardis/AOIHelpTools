class UpdateRecipeComponentsFromMash:

    def main(self, table: list, recipe_path: str):
        update_dictionary = self.get_components_for_update(table)
        #update_recipe(update_dictionary, recipe_path)
    @staticmethod
    def validate_table_for_update(table=[]):
        result = False
        if table:
            for component in table:
                if component[1] != 'empty' and component[2] != 'empty':
                    result = True
                    break
        return result

    @staticmethod
    def get_components_for_update(table: list):
        components_to_update = {}
        for item in table:
            if item[1] != 'empty' and item[2] != 'empty':
                components_to_update[item[0]] = item[2]
        return components_to_update
