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

- (void) imagePickerController:(UIImagePickerController *)picker didFinishPickingMediaWithInfo:(NSDictionary *)info {
    // Save the image as "cached.png" in a folder accessible by the app (user_data_dir in python/kivy)
    NSURL *ns_url = info[UIImagePickerControllerImageURL];
    // NSLog(@"the NSUrl path is %@", ns_url.path);

    NSLog(@"the NSUrl file is %@", ns_url.pathComponents.lastObject);


    UIImage *image = info[UIImagePickerControllerOriginalImage];
    NSData *imageData = UIImagePNGRepresentation(image);

    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *documentsDirectory = [paths objectAtIndex:0];

    NSString *imagePath = [documentsDirectory stringByAppendingPathComponent:[NSString stringWithFormat:@"%@.png",@"cached"]];

    NSLog(@"pre writing to file");
    if (![imageData writeToFile:imagePath atomically:NO])
    {
        NSLog(@"Failed to cache image data to disk");
    }
    else
    {
        NSLog(@"the cachedImagedPath is %@",imagePath);
    }
    [picker dismissViewControllerAnimated:YES completion:nil];//{
    // <#code#>
    //}];
}

@end