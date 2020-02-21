#import <Photos/Photos.h>

@interface NativeImagePicker : UIViewController
@property (strong, nonatomic) UIImagePickerController *imagePickerController;
@end
@implementation NativeImagePicker

-(id)init {
    NSLog(@"initializing NativeImagePicker");
    return self;
}

- (int)displayImagePicker {
    PHAuthorizationStatus status = [PHPhotoLibrary authorizationStatus];
    if(status == PHAuthorizationStatusNotDetermined) {
        // Request photo authorization
        [PHPhotoLibrary requestAuthorization:^(PHAuthorizationStatus status) {
            // User code (show imagepicker)
        }];
    } else if (status == PHAuthorizationStatusAuthorized) {
        // User code
    } else if (status == PHAuthorizationStatusRestricted) {
        // User code
    } else if (status == PHAuthorizationStatusDenied) {
        // User code
    }
    UIImagePickerController* imagePicker = [[UIImagePickerController alloc]init];
    // Check if image access is authorized
    if([UIImagePickerController isSourceTypeAvailable:UIImagePickerControllerSourceTypePhotoLibrary]) {
        imagePicker.sourceType = UIImagePickerControllerSourceTypePhotoLibrary;
        // Use delegate methods to get result of photo library -- Look up UIImagePicker delegate methods
        imagePicker.delegate = self;
        // Must show our imagepicker above the root view
        UIViewController *top = [UIApplication sharedApplication].keyWindow.rootViewController;
        [top presentViewController:imagePicker animated:YES completion: nil];
    }
    return 0;
}

- (NSString*) getFileName:(NSURL *) ns_url {
    // Return the file name without the path or file extention
    NSString *image_name = ns_url.pathComponents.lastObject;
    NSArray *listItems = [image_name componentsSeparatedByString:@"."];
    NSString *ret = listItems[0];
    return ret;
}

- (NSString*) getPNGFile {
    NSString* test = @"My NSString";
    return test;
}

- (NSString*) writeToPNG: (NSDictionary *) info {
    // Given the info frozen dictionary returned by the file picker, convert
    // the image selected to a PNG and return the full path.

    // Get the image name, stripped of path and extention
    NSString *image_name = [self getFileName: info[UIImagePickerControllerImageURL]];

    // Get the png representation of the image
    UIImage *image = info[UIImagePickerControllerOriginalImage];
    NSData *imageData = UIImagePNGRepresentation(image);

    // Generate the final image destination
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *documentsDirectory = [paths objectAtIndex:0];
    NSString *imagePath = [documentsDirectory stringByAppendingPathComponent:[NSString stringWithFormat:@"%@.png", image_name]];

    // Write the image data to the file
    if (![imageData writeToFile:imagePath atomically:NO])
    {
        NSLog(@"Failed to cache image data to disk");
        return @"";
    }
    else
    {
        NSLog(@"the cachedImagedPath is %@",imagePath);
        return imagePath;
    }

}

- (void) imagePickerController:(UIImagePickerController *)picker didFinishPickingMediaWithInfo:(NSDictionary *)info {
    // Save the image as "cached.png" in a folder accessible by the app (user_data_dir in python/kivy)
    // NSURL *ns_url = info[UIImagePickerControllerImageURL];
    // NSString *image_name = ns_url.pathComponents.lastObject;
    // NSArray *listItems = [image_name componentsSeparatedByString:@"."];
    // image_name = listItems[0];
    NSString *png_path = [self writeToPNG:info fileName: @"cached"];
    NSLog(@"Final image is %@", png_path);

    [picker dismissViewControllerAnimated:YES completion:nil];//{
    // <#code#>
    //}];
}

@end