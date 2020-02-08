import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from kivy.app import App
from kivy.utils import platform
if platform == 'ios':
    from pyobjus import autoclass
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty



class MainApp(App):
    native_image_picker = ObjectProperty(None)
    image_path = StringProperty("")

    def on_start(self):
        if platform == 'ios':
            self.native_image_picker = autoclass("NativeImagePicker").alloc().init()

    def update(self):
        print("Updating image...")

        folder = "/".join(x for x in self.user_data_dir.split("/")[:-1])
        image_path = folder + "/" + "cached.png"
        image = Image(source=image_path, nocache=True)
        self.root.add_widget(image)


    def pick_image(self):
        if platform == 'ios':
            self.native_image_picker.displayImagePicker()

MainApp().run()
