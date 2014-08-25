import warnings

warnings.warn(
    'DataGridBWC declarative is deprecated. Functionality has been moved to WebGrid.',
    DeprecationWarning,
    stacklevel=2
)

from webgrid import ExtractionError, DuplicateQueryNameError, Column, LinkColumnBase, \
    BoolColumn, YesNoColumn, DateColumnBase, DateColumn, DateTimeColumn, NumericColumn, \
    row_styler, col_styler, col_filter
from webgrid.blazeweb import Grid
