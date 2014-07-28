
def apply_patches():

    # Set default convertible types
    from collective.documentviewer.interfaces import IGlobalDocumentViewerSettings
    from collective.documentviewer.config import CONVERTABLE_TYPES
    IGlobalDocumentViewerSettings['auto_layout_file_types'].default = (
        CONVERTABLE_TYPES.keys()
    )
