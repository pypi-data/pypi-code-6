
def sjoin(left_df, right_df, op='intersects', how='left', **kwargs)
    """ Spatial join of two GeoDataFrames.

    left_df, right_df are GeoDataFrames (or GeoSeries)
    op: binary predicate {'intersects', 'contains', 'dwithin'}
    how: the type of join {'left', 'right', 'inner', 'outer'}
    left_cols, right_cols: optional lists of columns to include from each side
    kwargs: passed to op method
    """

    
