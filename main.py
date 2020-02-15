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
    native_image_picker = ObjectProperty(None)
    image_path = StringProperty("")

    def on_start(self):
        if platform == 'ios':
            self.native_image_picker = autoclass("NativeImagePicker").alloc().init()
        pass

    def update(self):
        print("Updating image...")

        folder = "/".join(x for x in self.user_data_dir.split("/")[:-1])
        image_path = folder + "/" + "cached.png"
        image = Image(source=image_path, nocache=True)
        self.root.add_widget(image)

    def callback(self):
        print("Callback fired!!!! ")

    def pick_image(self):
        # if platform == 'ios':
        #     print("Callign objective C picker")
        #     self.native_image_picker.callback = lambda: self.callback()
        #     self.native_image_picker.displayImagePicker()
        #     return

        picker = autoclass("UIImagePickerController",
                           copy_properties=False)
        picker_object = picker.alloc().init()

        picker_object.sourceType = 0 
        picker_object.delegate = self

        UIApplication = autoclass('UIApplication')
        vc = UIApplication.sharedApplication().keyWindow.rootViewController()

        vc.presentViewController_animated_completion_(picker_object, True, None)
        print("Called vc.presentViewController_animated_completion_")

    @protocol('UIImagePickerControllerDelegate')
    def imagePickerController_didFinishPickingMediaWithInfo_(self, *args):
        print("UIImagePickerControllerDelegate called")

    # @protocol("didFinishPickingMediaWithInfo")
    # def arb_name(self, *args):
    #     pass



MainApp().run()
