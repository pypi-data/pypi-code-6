from fanstatic import Group, Library, Resource

import js.bootstrap
import js.jquery
import js.jqueryui

library = Library('jquery_fileupload', 'resources')

ui_widget_js = Resource(
    library, 'js/vendor/jquery.ui.widget.js')

iframe_transport_js = Resource(
    library, 'js/jquery.iframe-transport.js',
    depends=[ui_widget_js],
)

fileupload_js = Resource(
    library, 'js/jquery.fileupload.js',
    depends=[
        js.bootstrap.bootstrap,
        js.jquery.jquery,
        iframe_transport_js,
    ],
)

fileupload_process_js = Resource(
    library, 'js/jquery.fileupload-process.js',
    depends=[
        fileupload_js,
    ],
)

fileupload_image_js = Resource(
    library, 'js/jquery.fileupload-image.js',
    depends=[
        fileupload_process_js,
    ],
)

fileupload_validate_js = Resource(
    library, 'js/jquery.fileupload-validate.js',
    depends=[
        fileupload_image_js,
    ],
)

fileupload_ui_css = Resource(
    library, 'css/jquery.fileupload-ui.css',
)

fileupload_css = Resource(
    library, 'css/jquery.fileupload.css',
)

fileupload_ui_js = Resource(
    library, 'js/jquery.fileupload-ui.js',
    depends=[
        fileupload_ui_css,
        fileupload_validate_js,
    ],
)

jquery_ui_fileupload = Group([
    fileupload_ui_js,
])

jquery_fileupload = Group([
    fileupload_validate_js,
    fileupload_css,
])
