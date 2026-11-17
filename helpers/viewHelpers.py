import createWindow as ui


class ViewHelper:

    def generate_layout_for_path_browsers(
            self,
            input_layouts,
            text_background_color=None,
            folder_browser=True,
            stored_input=None
    ):
        if stored_input is None:
            stored_input = {}
        layouts = []

        for val in input_layouts:
            val_to_upper_case = val.upper().replace(' ', '_')
            val_first_upper_case = val.capitalize()
            name = '-' + val_to_upper_case + '_PATH-'
            default_text = '' if not stored_input else stored_input[name]
            browse = ui.folder_browse() if folder_browser else ui.file_browse()
            layouts.append([
                ui.text(val_first_upper_case + ' path', text_background_color, width=34),
                ui.input_box(name, default=default_text, enable_events=True, expand=True),
                browse,
            ])
        return layouts
