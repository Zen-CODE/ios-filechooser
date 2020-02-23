from kivy.app import App
from kivy.uix.image import Image
from filechooser import IOSFileChooser


class MainApp(App):

    def add_image(self, selection):
        """ Add an image to the UI given the sepecified `image_path`. """
        if selection:
            self.root.add_widget(Image(source=selection[0], nocache=True))
        else:
            print("Called but with empty list.")

    def pick_image(self):
        filechooser = IOSFileChooser()
        filechooser.open_file(on_selection=self.add_image)


MainApp().run()
