import kivy
kivy.require('1.8.0')
import os
from kivy.metrics import dp
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from filebrowser import FileBrowser
from fish_types import fishes, fish_codes, substrate_types
from file_processor import FileProcessor


class FilePopup(Popup):
    def __init__(self, on_success, title="Select File", name_filter="*.*", **kwargs):
        super(FilePopup, self).__init__(title=title, **kwargs)


        self.browser = FileBrowser(select_string='Select', filters=[name_filter])
        self.browser.bind(
                    on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled)

        self.on_success_callback = on_success

        self.content = self.browser

        self.selected_file = None

    def _fbrowser_canceled(self, instance):
        self.dismiss()

    def _fbrowser_success(self, instance):
        self.dismiss()
        if self.browser.selection is not []:
            self.selected_file = self.browser.selection[0]
            self.on_success_callback(self.selected_file)


class FileDropDown(DropDown):
    pass

class OptionsDropDown(DropDown):
    pass

class FishBubbleButtons(GridLayout):
    pass

class MainWindow(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''

    image_scale = ObjectProperty()

    main_image_source = StringProperty()
    next_button_image_source = StringProperty()
    prev_button_image_source = StringProperty()
    current_image_num = StringProperty()
    total_num_images = StringProperty()

    image_data = ObjectProperty()

    def __init__(self, app, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.app = app
        self.add_fishes()
        self.populate_substrates()

        self.processor = FileProcessor()

        self.file_popup = FilePopup(on_success=self.refresh_from_file, name_filter="*.txt")
        self.file_dropdown = FileDropDown()
        self.options_dropdown = OptionsDropDown()

    def add_fishes(self):


        for fish_type in fishes.keys():
            #group_button = ToggleButton(text=fish_group, group='fish_group')
            #self.ids.fish_group_box.add_widget(group_button)

            number_of_types = len(fishes[fish_type])
            number_of_rows = number_of_types / 2 + 1

            this_tab_item = TabbedPanelItem(text=fish_type)
            buttons_scrollview = ScrollView(do_scroll_x=False, size_hint=(1,1))
            button_grid = GridLayout(cols=2, rows=number_of_rows, row_default_height=dp(30), row_force_default=True, size_hint=(1, None))
            button_grid.bind(minimum_height = button_grid.setter('height'))
            this_tab_item.add_widget(buttons_scrollview)
            buttons_scrollview.add_widget(button_grid)

            this_tab_item.subtype_buttons = []
            for fish_subtype in fishes[fish_type]:
                type_button = ToggleButton(text=fish_subtype, group=fish_type)
                type_button.bind(on_release=self.set_fish_type)
                button_grid.add_widget(type_button)

                # Also add a referece to this button to the tabbedpanelitem so we can easily find it later.
                this_tab_item.subtype_buttons.append(type_button)

            button_grid.children[-1].state = 'down'

            self.ids.fish_type_panel.add_widget(this_tab_item)

        # Now, add the "Other" tab.
        #this_tab_item = TabbedPanelItem(text="Other")
        self.fish_type_other_textbox = TextInput(id='fish_type_other_textbox', width=dp(300), height=dp(30), size_hint_y=None, multiline=False)
        self.fish_type_other_textbox.bind(text=self.set_fish_type)
        #this_tab_item.add_widget(fish_type_other_textbox)
        self.ids.fish_type_panel.default_tab_content = self.fish_type_other_textbox

        # And select the first tab.  (0 is the "default tab".  Why? Kivy hates us, that's why.
        #self.ids.fish_type_panel.switch_to(self.ids.fish_type_panel.tab_list[1])

        # Now, bind an event when the tab changes
        self.ids.fish_type_panel.bind(current_tab=self.set_fish_type)

    def populate_substrates(self):
        for spinner in (self.ids.substrate_spinner_1, self.ids.substrate_spinner_2):
            spinner.values = substrate_types

        self.ids.substrate_spinner_1.values.append('not classified')
        self.ids.substrate_spinner_1.text = 'not classified'
        self.ids.substrate_spinner_2.values.append('')
        self.ids.substrate_spinner_2.text = ''



    def start_length(self):
        self.ids.paint_widget.drawing_state.is_drawing = True

    def set_fish_type(self, *args):
        # get the selected tab
        fish_type = self.ids.fish_type_panel.current_tab.text



        fish_subtype = ""

        if fish_type == "Other":
            fish_code = "OT"
            fish_subtype = self.fish_type_other_textbox.text
        else:
            # !#$% Kivy and its asinine default tab
            if fish_type not in fish_codes.keys():
                return

            fish_code = fish_codes[fish_type]
            for button in self.ids.fish_type_panel.current_tab.subtype_buttons:
                if button.state == 'down':
                    fish_subtype = button.text

        self.ids.paint_widget.drawing_state.current_type = fish_type
        self.ids.paint_widget.drawing_state.current_subtype = fish_subtype
        self.ids.paint_widget.drawing_state.current_code = fish_code

    def on_count_press(self):
        state = True if (self.ids.count_button.state == 'down') else False

        if state:
            self.ids.paint_widget.start_count()
        if not state:
            self.ids.panzoom_button.state = 'down'
            self.ids.paint_widget.stop_count()

    def set_zoom_100(self):
        self.ids.image_scatter.scale = 1.0

    def set_zoom_in(self):
        self.ids.image_scatter.scale *= 1.25

    def set_zoom_out(self):
        self.ids.image_scatter.scale *= 0.75

    def set_zoom_fit(self):
        im_width = float(self.ids.image_widget.texture_size[0])
        im_height = float(self.ids.image_widget.texture_size[1])

        view_height = self.ids.image_view.height
        view_width = self.ids.image_view.width

        # figure out the ideal scale factors in each direction
        scale_width = view_width / im_width
        scale_height = view_height / im_height

        # pick the minimum to actually apply
        self.ids.image_scatter.scale = min([scale_height, scale_width])

        self.repos_image()

    def enable_font_scaling(self, is_enabled):
        if self.ids.paint_widget.font_scale_enabled != is_enabled:
            self.ids.paint_widget.font_scale_enabled = is_enabled
            self.refresh_from_processor()

    def next_button_on_press(self):
        self.save_current_annotations()
        self.processor.go_to_next()
        self.refresh_from_processor()
        self.set_zoom_fit()

    def previous_button_on_press(self):
        self.save_current_annotations()
        self.processor.go_to_previous()
        self.refresh_from_processor()
        self.set_zoom_fit()

    def save_current_annotations(self):
        # save our points
        self.processor.current_fish_points = list(self.ids.paint_widget.fish_points)
        # and the other stuff
        self.processor.current_entry['comment'] = self.ids.comment_text_input.text

        # this is ugly...
        if self.ids.substrate_spinner_1.text is "not classified":
            self.processor.current_entry['substrate'] = "not classified"
        else:
            self.processor.current_entry['substrate'] = \
                self.ids.substrate_spinner_1.text + self.ids.substrate_spinner_2.text


    def update_substrate_spinners(self):
        # This is an awful hack.
        code = self.processor.current_entry['substrate']
        num_chars = len(code)
        if num_chars < 3:
            if num_chars == 2:
                self.ids.substrate_spinner_2.text = code[1]
            else:
                self.ids.substrate_spinner_2.text = ""
            self.ids.substrate_spinner_1.text = code[0]
        else:
            self.ids.substrate_spinner_1.text = code
            self.ids.substrate_spinner_2.text = ""



    def repos_image(self, x=0, y=0):
        self.ids.image_scatter._set_pos((x,y))

    def open_telem_file(self):
        self.file_popup.open()

    def refresh_from_file(self, selected_file):
        if selected_file is not None:
            self.processor.read_telem_file(selected_file)
            self.refresh_from_processor()

        self.set_zoom_fit()


    def fast_telem_file(self):
        self.processor.read_telem_file('c:/users/eric/code/pyfishrock/sample_dive/d20131129_dive6_telem.txt')
        self.refresh_from_processor()

    def export_image(self):
        if self.processor.current_entry:
            file_name = ('.').join(self.processor.current_entry['image'].split('.')[:-1]) + '.png'
            export_name = os.path.join(self.processor.image_directory, file_name)
        self.ids.image_layout.export_to_png(export_name)

    def refresh_from_processor(self):
        if self.processor.file_is_loaded:
            self.main_image_source = self.processor.get_current_image_pathname()
            self.next_button_image_source = self.processor.get_next_image_pathname()
            self.prev_button_image_source = self.processor.get_prev_image_pathname()
            self.ids.paint_widget.fish_points = self.processor.current_fish_points
            self.ids.paint_widget.refresh()
            self.total_num_images = str(self.processor.number_of_images)
            self.current_image_num = str(self.processor.current_index + 1)
            self.image_data = self.processor.current_entry
            self.ids.paint_widget.telem_entry = self.processor.current_entry
            self.update_substrate_spinners()


class OneTwoRedBlueApp(App):

    def build(self):
        self.icon = 'twofish.png'
        main_window = MainWindow(app=self)
        return main_window

def run_application():
    OneTwoRedBlueApp().run()

if __name__ == '__main__':

    OneTwoRedBlueApp().run()