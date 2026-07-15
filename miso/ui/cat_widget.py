from kivy.uix.image import Image

from miso.config import ASSETS_FOLDER


class CatWidget(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = str(ASSETS_FOLDER / "cat_idle.gif")

        self.size_hint = (None, None)
        self.size = (180, 180)

        # Controls the speed of the GIF.
        self.anim_delay = 0.1

        # Zero makes the GIF loop continuously.
        self.anim_loop = 0