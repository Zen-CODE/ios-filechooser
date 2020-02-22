'''
iOS file chooser
--------------------

.. versionadded:: 1.4.0  # TODO
'''

from plyer.facades import FileChooser
# from plyer import storagepath


class IOSFileChooser(FileChooser):
    '''
    FileChooser implementation for IOS using
    the built-in file browser via UIImagePNGRepresentation.

    .. versionadded:: 1.4.0
    '''

    def __init__(self, *args, **kwargs):
        super(IOSFileChooser, self).__init__(*args, **kwargs)

    def _file_selection_dialog(self, **kwargs):
        pass
