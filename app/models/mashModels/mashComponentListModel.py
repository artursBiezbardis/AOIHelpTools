import app.models.mashModels.mashComponentModel as componentModel


class MashComponentListModel:

    def __init__(self, mash_file_data):

        self.mash_file_data = mash_file_data
        self.components_top = []
        self.components_bot = []
        self.components_mount = []
        self.components_flip = []
        self.components_comment = []
        self.components_fid_top = []
        self.components_fid_bot = []
        self.components_smt = []
        self.components_hmt = []
        self.components_tht = []
        self.attributes = {}
        self.component_dict = self.create_component_dict()
        self.get_component_filter_dict()

    def create_component_dict(self):
        component_dict = {}
        for key, mash_component in self.mash_file_data.items():
            key.strip()
            component = componentModel.MashComponentModel(mash_component)
            component_dict[key] = component
            if isinstance(component.get_side(), str) and 'top' in (component.get_side()).lower():
                self.components_top.append(key)
            if isinstance(component.get_side(), str) and 'bot' in (component.get_side()).lower():
                self.components_bot.append(key)
            if isinstance(component.get_mount(), str) and 'yes' in (component.get_mount()).lower():
                self.components_mount.append(key)
            if isinstance(component.get_comment(), str) and 'flip' in (component.get_comment()).lower() \
                    or isinstance(component.get_description(), str) and 'flip' in (component.get_description()).lower():
                self.components_flip.append(key)
            if isinstance(component.get_comment(), str):
                self.components_comment.append(key)
            if 'FM' in key and 'top' in (component.get_side()).lower():
                self.components_fid_top.append(key)
            if 'FM' in key and 'top' in (component.get_side()).lower():
                self.components_fid_top.append(key)

            if isinstance(component.get_mount_type(), str) and 'smt' in (component.get_mount_type()).lower():
                self.components_smt.append(key)
            if isinstance(component.get_mount_type(), str) and 'hmt' in (component.get_mount_type()).lower():
                self.components_hmt.append(key)
            if isinstance(component.get_mount_type(), str) and 'tht' in (component.get_mount_type()).lower():
                self.components_tht.append(key)

        return component_dict

    def get_components(self, selectors: [str]=[], remove: [str]=[] ):
        """
        This is method returns selected mash components, by specific mash data type

        Parameters:
            selectors ([(str),(str)...]) optional selections:
             'top' - select all top mount components
             'bot' - select all bot mount components
             'mount' - selects components that's mounts on board
             'flip' - selects flip mount components
             'comments' - selects components with comments
             'fid_top' - selects top fiducials
             'fid_bot' - selects bot fiducials
             'smt' - selects smt components
             'hmt' - selects hmt components
             'tht' - selects tht components

                Usage description:
                    function iterates via selectors on each selector selects all matching component by names

            remove ([(str),(str)...]) optional selections:
             'top' - removes all top mount components
             'bot' - removes all bot mount components
             'mount' - removes components that's mounts on board
             'flip' - removes flip mount components
             'comments' - removes components with comments
             'fid_top' - removes top fiducials
             'fid_bot' - removes bot fiducials
             'smt' - removes smt components
             'hmt' - removes hmt components
             'tht' - removes tht components

                Usage description:
                    function iterates via remove list on each selector removes all matching component by names


        Returns:
              dictionary with selected and removed components

        """
        filter_dict = self.get_component_filter_dict()

        selected_components = self.component_dict
        results = {}
        if selectors:
            for selection in selectors:
                selected_component_keys = filter_dict[selection]

                for component_key in selected_component_keys:
                    if component_key in selected_components:
                        results[component_key] = selected_components[component_key]
            selected_components = results
        if remove:
            for selection in remove:
                selected_component_keys = filter_dict[selection]

                for component_key in selected_component_keys:
                    if component_key in selected_components:
                        del selected_components[component_key]

        return selected_components

    def get_component_filter_dict(self):

        return {'top': self.components_top,
                'bot': self.components_bot,
                'mount': self.components_mount,
                'flip': self.components_flip,
                'comment': self.components_comment,
                'fid_top': self.components_fid_top,
                'fid_bot': self.components_fid_bot,
                'smt': self.components_smt,
                'hmt': self.components_hmt,
                'tht': self.components_tht}

    def get_attributes(self):

        return self.attributes

    def set_attribute(self, key, value):

        self.attributes[key] = value
