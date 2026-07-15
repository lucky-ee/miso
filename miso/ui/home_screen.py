from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from miso.services.storage import save_cat
from miso.ui.cat_widget import CatWidget


class HomeScreen(FloatLayout):
    def __init__(self, cat, **kwargs):
        super().__init__(**kwargs)

        self.cat_model = cat
        self._message_event = None

        self.cat_widget = CatWidget(
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.48,
            },
        )
        self.add_widget(self.cat_widget)

        self.name_label = Label(
            text=self.cat_model.name,
            font_size=28,
            size_hint=(0.4, 0.1),
            pos_hint={"x": 0.05, "top": 0.98},
        )
        self.add_widget(self.name_label)

        self.stats_label = Label(
            text=self.get_statistics_text(),
            font_size=18,
            size_hint=(0.9, 0.1),
            pos_hint={"center_x": 0.5, "y": 0.78},
        )
        self.add_widget(self.stats_label)

        self.message_label = Label(
            text="",
            font_size=16,
            size_hint=(0.9, 0.08),
            pos_hint={"center_x": 0.5, "y": 0.68},
        )
        self.add_widget(self.message_label)

        self.create_buttons()

        Clock.schedule_interval(self.update_cat, 1)

    def create_buttons(self):
        feed_button = Button(
            text="Feed",
            size_hint=(0.22, 0.09),
            pos_hint={"x": 0.02, "y": 0.03},
        )
        feed_button.bind(on_release=self.feed_cat)
        self.add_widget(feed_button)

        pet_button = Button(
            text="Pet",
            size_hint=(0.22, 0.09),
            pos_hint={"x": 0.27, "y": 0.03},
        )
        pet_button.bind(on_release=self.pet_cat)
        self.add_widget(pet_button)

        play_button = Button(
            text="Play",
            size_hint=(0.22, 0.09),
            pos_hint={"x": 0.52, "y": 0.03},
        )
        play_button.bind(on_release=self.play_with_cat)
        self.add_widget(play_button)

        groom_button = Button(
            text="Groom",
            size_hint=(0.22, 0.09),
            pos_hint={"x": 0.77, "y": 0.03},
        )
        groom_button.bind(on_release=self.groom_cat)
        self.add_widget(groom_button)

    def get_statistics_text(self):
        return (
            f"Fullness: {int(self.cat_model.fullness)}    "
            f"Affection: {int(self.cat_model.affection)}"
        )

    def update_statistics(self):
        self.stats_label.text = self.get_statistics_text()

    def show_message(self, message):
        self.message_label.text = message

        if self._message_event is not None:
            self._message_event.cancel()

        self._message_event = Clock.schedule_once(
            self.clear_message,
            3,
        )

    def clear_message(self, _seconds):
        self.message_label.text = ""
        self._message_event = None

    def feed_cat(self, _instance):
        if self.cat_model.fullness >= 95:
            self.show_message(
                f"{self.cat_model.name} is already full!"
            )
            return

        self.cat_model.fullness = min(
            100,
            self.cat_model.fullness + 20,
        )

        self.show_message(
            f"You fed {self.cat_model.name}."
        )

        self.finish_action()

    def pet_cat(self, _instance):
        self.cat_model.affection = min(
            100,
            self.cat_model.affection + 3,
        )

        self.show_message(
            f"{self.cat_model.name} enjoyed that!"
        )

        self.finish_action()

    def play_with_cat(self, _instance):
        self.show_message(
            "Play options are coming next!"
        )

    def groom_cat(self, _instance):
        self.show_message(
            "Grooming options are coming next!"
        )

    def finish_action(self):
        self.update_statistics()
        save_cat(self.cat_model)

    def update_cat(self, _seconds):
        self.cat_model.fullness = max(
            0,
            self.cat_model.fullness - 0.02,
        )

        self.update_statistics()