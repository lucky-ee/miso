from miso.app import VirtualCatApp


if __name__ == "__main__":
    VirtualCatApp().run()

class MisoApp(App):
    def build(self):
        return CatRoom()


if __name__ == "__main__":
    MisoApp().run()