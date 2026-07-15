from kivy.app import App
from kivy.core.window import Window

from miso.models.cat import Cat
from miso.services.storage import load_cat
from miso.ui.home_screen import HomeScreen


Window.size = (400, 700)


class VirtualCatApp(App):
    def build(self):
        cat = load_cat()

        if cat is None:
            cat = Cat(name="Miso")

        return HomeScreen(cat=cat)

    def on_stop(self):
        if self.root is not None:
            from miso.services.storage import save_cat

            save_cat(self.root.cat_model)