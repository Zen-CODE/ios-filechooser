import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from kivy.app import App
from kivy.utils import platform
if platform == 'ios':
    from pyobjus import autoclass, protocol, ObjcVoid, objc_i
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty
from pyobjus.dylib_manager import load_framework

load_framework('/System/Library/Frameworks/Photos.framework')

class MainApp(App):
    picker = None

    def update(self):
        print("Updating image...")

        folder = "/".join(x for x in self.user_data_dir.split("/")[:-1])
        image_path = folder + "/" + "cached.png"
        image = Image(source=image_path, nocache=True)
        self.root.add_widget(image)

    def _get_picker(self):
        """
        Return an instantiated and configured UIImagePickerController.
        """
        picker = autoclass("UIImagePickerController")
        po = picker.alloc().init()
        po.sourceType = 0 
        po.delegate = self
        return po

    def pick_image(self):
        self.picker = self._get_picker()
        UIApplication = autoclass('UIApplication')
        vc = UIApplication.sharedApplication().keyWindow.rootViewController()

        vc.presentViewController_animated_completion_(self.picker, True, None)
        print("Called vc.presentViewController_animated_completion_")

    @protocol('UIImagePickerControllerDelegate')
    def imagePickerController_didFinishPickingMediaWithInfo_(
            self, image_picker, frozen_dict):
        print(f"UIImagePickerControllerDelegate called: {frozen_dict}")




MainApp().run()
