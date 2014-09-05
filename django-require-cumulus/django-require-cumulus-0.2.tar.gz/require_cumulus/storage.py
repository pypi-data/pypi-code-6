from cumulus.storage import SwiftclientStaticStorage
from django.contrib.staticfiles.storage import StaticFilesStorage
from require.storage import OptimizedFilesMixin


class RequireSwiftStaticStorage(OptimizedFilesMixin, StaticFilesStorage,
                                SwiftclientStaticStorage):
    pass
