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
        """
        Launch the native iOS file browser. Upon selection, the
        `imagePickerController_didFinishPickingMediaWithInfo_` delegate is
        called where we close the file browser and handle the result.
        """
        self.picker = self._get_picker()
        UIApplication = autoclass('UIApplication')
        vc = UIApplication.sharedApplication().keyWindow.rootViewController()

        vc.presentViewController_animated_completion_(self.picker, True, None)
        print("Called vc.presentViewController_animated_completion_")

    @protocol('UIImagePickerControllerDelegate')
    def imagePickerController_didFinishPickingMediaWithInfo_(
            self, image_picker, frozen_dict):
        """
        Delegate which handles the result of the image seletion process.
        """
        image_picker.dismissViewControllerAnimated_completion_(True, None)

        all_keys = frozen_dict.allKeys()  # NSArrayI
        # object at 0 = UIImagePickerControllerMediaType
        # object at 1 = UIImagePickerControllerOriginalImage
        # object at 2 = UIImagePickerControllerReferenceURL
        # object at 3 = UIImagePickerControllerImageURL
        # object at 4 = UIImagePickerControllerPHAsset
        # print(f"all_keys = {all_keys}")
        # try:
        #     k = 0
        #     while True:
        #         obj = all_keys.objectAtIndex_(k)
        #         print(f"object at {k} = {obj.UTF8String()}")
        #         k += 1
        # except Exception as _e:
        #     pass

        # print(all_keys.size())

        NSString = autoclass('NSString')
        string_key = NSString.stringWithUTF8String_(
            "UIImagePickerControllerImageURL")
        obj = frozen_dict.objectForKey_(string_key)
        print(f"Got UIImage {obj}")  # <__main__.NSURL object at 0x1229c31a8>

        # # we can iterate over dict values
        # enumerator = frozen_dict.objectEnumerator()
        # obj = enumerator.nextObject()
        # while obj:
        #     str_value = obj.pngData()
        #     print("Value: " + str_value)
        #     obj = enumerator.nextObject()

        # NSString = autoclass('NSString')
        # string_key = NSString.stringWithUTF8String_("imageURL")
        # ret = frozen_dict.objectForKey_(string_key)
        # print(f"ret = {ret}")

MainApp().run()
