import os
import time

from kerykeion import AstrologicalSubject, KerykeionChartSVG
from geocode.geolocs import GeoCountry
from geocode.country_codes import COUNTRY_CODES

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker, MDTimePicker


def convert_svg_to_png(svg_file, png_file, resolution = 144):
    from wand.api import library
    import wand.color
    import wand.image

    print('Turning {} into {}'.format(svg_file, png_file))
    with open(svg_file, 'r', encoding='utf-8') as svg_file_contents:
        with wand.image.Image() as image:
            with wand.color.Color('transparent') as background_color:
                library.MagickSetBackgroundColor(image.wand, background_color.resource)
            svg_blob = svg_file_contents.read().encode('utf-8')
            image.read(blob=svg_blob, resolution = resolution)
            png_image = image.make_blob("png32")

    try:
        os.remove(png_file)
    except OSError:
        pass

    with open(png_file, "wb") as out:
        out.write(png_image)

    try:
        os.remove(svg_file)
    except OSError:
        pass

class StartWidget(FloatLayout):
    pass

class DatePickerWidget(FloatLayout):
    pass

class ChartDisplayWidget(FloatLayout):
    pass

class GalacticatApp(MDApp):
    country_obj = GeoCountry('US')
    image_popup = Popup(title='Chart', size_hint=(1, 1))

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            # Android Back button and PC ESC button
            print('ESC/Back hit')
            try:
                self.image_popup.dismiss()
            except Exception:
                pass
            return True

    def build(self):
        return StartWidget()

    def on_date_picker_save(self, instance, value, date_range):
        App.get_running_app().root.ids.birth_date_input.text = str(value)

    def on_date_picker_cancel(self, instance, value):
        pass

    def on_time_picker_save(self, instance, value):
        App.get_running_app().root.ids.birth_time_input.text = str(value)

    def on_time_picker_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_picker_save, on_cancel=self.on_date_picker_cancel)
        date_dialog.open()

    def show_time_picker(self):
        date_dialog = MDTimePicker()
        date_dialog.bind(on_save=self.on_time_picker_save, on_cancel=self.on_time_picker_cancel)
        date_dialog.open()

    def text_suggestions_country(self, instance, value):
        max_suggestions = 5
        word_list = [k for k, v in COUNTRY_CODES.items()]
        instance.hint_text = 'Type a country name'
        instance.helper_text = ''
        potential_words = [w for w in word_list if w.startswith(value)]
        if len(potential_words) == 1:
            value = potential_words[0]
            instance.text = value
            print('Auto-complete to only match: {}'.format(value))
        exact_match = any(w for w in word_list if value == w)
        if potential_words:
            if exact_match:
                instance.hint_text = 'Chosen Country: {}'.format(value)
                instance.helper_text = 'Chosen Country: {}'.format(', '.join(potential_words))
                print('Loading Country Object for: {} - {}'.format(value, COUNTRY_CODES[value]))
                self.country_obj = GeoCountry(COUNTRY_CODES[value])
                print(self.country_obj)
            if len(potential_words) <= max_suggestions:
                instance.helper_text = 'Suggestions: {}'.format(', '.join(potential_words))
            elif len(potential_words) > max_suggestions:
                instance.helper_text = 'Suggestions: {}'.format(', '.join(potential_words[0: max_suggestions]))

    def text_suggestions_state(self, instance, value):
        max_suggestions = 5
        country_text = App.get_running_app().root.ids.country_input.text
        instance.hint_text = 'Type a state name'
        if not country_text in COUNTRY_CODES:
            instance.helper_text = 'Please enter a valid Country first'
            return
        print(self.country_obj)
        word_list = [k for k in self.country_obj.states()]
        instance.helper_text = ''
        potential_words = [w for w in word_list if w.startswith(value)]
        if len(potential_words) == 1:
            value = potential_words[0]
            instance.text = value
            print('Auto-complete to only match: {}'.format(value).encode('utf-8'))
        exact_match = any(w for w in word_list if value == w)
        if potential_words:
            if exact_match:
                instance.hint_text = 'Chosen State: {}'.format(value)
                instance.helper_text = 'Chosen State: {}'.format(', '.join(potential_words))
            if len(potential_words) <= max_suggestions:
                instance.helper_text = 'Suggestions: {}'.format(', '.join(potential_words))
            elif len(potential_words) > max_suggestions:
                instance.helper_text = 'Suggestions: {}'.format(', '.join(potential_words[0: max_suggestions]))

    def text_suggestions_city(self, instance, value):
        max_suggestions = 5
        country_text = App.get_running_app().root.ids.country_input.text
        state_text = App.get_running_app().root.ids.state_input.text
        instance.hint_text = 'Type a city name'
        if not country_text in COUNTRY_CODES:
            instance.helper_text = 'Please enter a valid Country first'
            return
        word_list = [k for k in self.country_obj.cities(state_text)]
        instance.helper_text = ''
        potential_words = [w for w in word_list if w.startswith(value)]
        if len(potential_words) == 1:
            value = potential_words[0]
            instance.text = value
            print('Auto-complete to only match: {}'.format(value.encode('utf-8')))
        exact_match = any(w for w in word_list if value == w)
        if potential_words:
            if exact_match:
                instance.hint_text = 'Chosen City: {}'.format(value)
                instance.helper_text = 'Chosen City: {}'.format(', '.join(potential_words))
            if len(potential_words) <= max_suggestions:
                instance.helper_text = 'Suggestions: {}'.format(', '.join(potential_words))
            elif len(potential_words) > max_suggestions:
                instance.helper_text = 'Suggestions: {}'.format(', '.join(potential_words[0: max_suggestions]))


    def generate_chart(self):
        name_text = App.get_running_app().root.ids.name_input.text
        print('Generating Chart for {}'.format(name_text).encode('utf-8'))
        birth_date_text = App.get_running_app().root.ids.birth_date_input.text
        birth_time_text = App.get_running_app().root.ids.birth_time_input.text
        country_text = App.get_running_app().root.ids.country_input.text
        state_text = App.get_running_app().root.ids.state_input.text
        city_text = App.get_running_app().root.ids.city_input.text

        year = int(birth_date_text.split('-')[0])
        month = int(birth_date_text.split('-')[1])
        day = int(birth_date_text.split('-')[2])
        hour = int(birth_time_text.split(':')[0])
        minute = int(birth_time_text.split(':')[1])

        geo_loc = self.country_obj.get_geo_loc(state_text, city_text)

        astro_subject_data = {
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute,
            'city': city_text,
            'nation': country_text,
            'lng': geo_loc.longitude,
            'lat': geo_loc.latitude,
            'tz_str': 'America/New_York',
            'geonames_username': 'APerson'
        }
        print('Making Chart for {}: [{}]'.format(name_text, astro_subject_data).encode('utf-8'))

        astro_subject = AstrologicalSubject(name_text, **astro_subject_data)
        natal_chart = KerykeionChartSVG(astro_subject, "Natal", new_output_directory=".")
        natal_chart.makeSVG()

        chart_file_name = "{} - Natal Chart".format(name_text)
        convert_svg_to_png(chart_file_name + '.svg', 'recent_chart' + '.png')
        self.popup_image()

    def popup_image(self):
        content = Image(source='recent_chart.png')
        self.image_popup.content = content
        self.image_popup.open()



if __name__ == '__main__':
    GalacticatApp().run()