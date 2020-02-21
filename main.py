import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from kivy.app import App
from kivy.utils import platform
if platform == 'ios':
    from pyobjus import autoclass, protocol, ObjcVoid, objc_i
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty
from pyobjus.dylib_manager import load_framework, INCLUDE

load_framework('/System/Library/Frameworks/Photos.framework')
# load_framework('/System/Library/Frameworks/UIKit.framework')
#  load_framework(INCLUDE.UIKit)


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
        # native_image_picker = autoclass("NativeImagePicker").alloc().init()
        # native_image_picker.displayImagePicker()
        # val = native_image_picker.getPNGFile().UTF8String()
        # print(f"Got NativeImagePicker {val}")
        # return

        self.picker = self._get_picker()
        UIApplication = autoclass('UIApplication')
        vc = UIApplication.sharedApplication().keyWindow.rootViewController()

        vc.presentViewController_animated_completion_(self.picker, True, None)
        print("Called vc.presentViewController_animated_completion_")

    @staticmethod
    def get_ffd(fdict, key):
        """ Retrieve the obejct with the specified key from the frozen dict.
        """
        NSString = autoclass('NSString')
        string_key = NSString.stringWithUTF8String_(key)
        return fdict.objectForKey_(string_key)

    @protocol('UIImagePickerControllerDelegate')
    def imagePickerController_didFinishPickingMediaWithInfo_(
            self, image_picker, frozen_dict):
        """
        Delegate which handles the result of the image seletion process.
        """
        image_picker.dismissViewControllerAnimated_completion_(True, None)

        # all_keys = frozen_dict.allKeys()  # NSArrayI
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

        NSString = autoclass('NSString')
        file_name = NSString.stringWithUTF8String_("file_name")
        native_image_picker = autoclass("NativeImagePicker").alloc().init()

        print("About to call writeToPNG.")
        path = native_image_picker.writeToPNG_fileName_(frozen_dict, file_name)
        print(f"writeToPNG returned {path}")


        # imageURL = self.get_ffd(frozen_dict, "UIImagePickerControllerImageURL")
        # print(f"Got imageURL {imageURL}")  # NSURL object

        # image = self.get_ffd(frozen_dict,
        #                      "UIImagePickerControllerOriginalImage")
        # print(f"Got image {image}")  # UIImage object

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
