from kivy.app import App
from pyobjus import autoclass, protocol
from kivy.uix.image import Image
from pyobjus.dylib_manager import load_framework

load_framework('/System/Library/Frameworks/Photos.framework')


class MainApp(App):

    def add_image(self, image_path):
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
        """
        Launch the native iOS file browser. Upon selection, the
        `imagePickerController_didFinishPickingMediaWithInfo_` delegate is
        called where we close the file browser and handle the result.
        """
        picker = self._get_picker()
        UIApplication = autoclass('UIApplication')
        vc = UIApplication.sharedApplication().keyWindow.rootViewController()
        vc.presentViewController_animated_completion_(picker, True, None)

    @protocol('UIImagePickerControllerDelegate')
    def imagePickerController_didFinishPickingMediaWithInfo_(
            self, image_picker, frozen_dict):
        """
        Delegate which handles the result of the image seletion process.
        """
        image_picker.dismissViewControllerAnimated_completion_(True, None)

        native_image_picker = autoclass("NativeImagePicker").alloc().init()
        path = native_image_picker.writeToPNG_(frozen_dict)
        print(f"writeToPNG returned {path.UTF8String()}")
        self.add_image(path.UTF8String())


MainApp().run()
