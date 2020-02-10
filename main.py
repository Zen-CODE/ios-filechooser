import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from kivy.app import App
from kivy.utils import platform
if platform == 'ios':
    from pyobjus import autoclass, protocol, ObjcVoid, objc_i
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty
from pyobjus.dylib_manager import load_framework



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
        # if platform == 'ios':
        #     self.native_image_picker.displayImagePicker()
        picker = autoclass(
            "UIImagePickerController",
            load_class_methods=[b'alloc'],
            load_instance_methods=[b'init', b'setSourceType_'])
        print("Created UIImagePickerController..")

        picker_object = picker.alloc().init()
        print(f"picker_object = {picker_object}")

        # picker_object.sourceType = objc_i(0) - give  TypeError: an integer
        # is required (got type __NSCFNumber)
        picker_object.sourceType = 0 
        print("picker_object.sourceType = objc_i(0)")

        # picker_object.sourceType = picker_object.SourceType.photoLibrary
        picker_object.delegate = self
        print("Picker delegate set")

        UIApplication = autoclass('UIApplication')
        vc = UIApplication.sharedApplication().keyWindow.rootViewController()

        print(f"vc alloced and inited = {vc}")
        # print(f"vc has {dir(vc)}")

        # vc.presentViewController_animated_completion_(picker, objc_b(True), objc_b(True))
        # vc.presentViewController_animated_completion_(picker, True, ObjcVoid(None))
        vc.presentViewController_animated_completion_(picker_object, True, None)
        print("Removing valid picker_object V2")
        # vc.presentViewController_animated_completion_(True, True, None)

        # load_framework('/System/Library/Frameworks/Photos.framework')
        #print("loaded Photolib framework..")

    @protocol('UIImagePickerControllerDelegate')
    def imagePickerController_didFinishPickingMediaWithInfo_(self, *args):
        print("UIImagePickerControllerDelegate called")

    # @protocol("didFinishPickingMediaWithInfo")
    # def arb_name(self, *args):
    #     pass



MainApp().run()
