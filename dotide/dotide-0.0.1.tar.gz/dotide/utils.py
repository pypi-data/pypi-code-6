from datetime import datetime


def parse_datetime(dt):
    """Parse iso8601 format UTC time to datetime."""
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")


def format_time(v):
    """Format time."""
    return v.isoformat() + 'Z' if isinstance(v, datetime) else v


def format_params(params):
    """Format params."""
    def _coerce(v):
        if isinstance(v, list):
            return ','.join(v)
        elif isinstance(v, datetime):
            return v.isoformat() + 'Z'
        else:
            return v
    return {k: _coerce(params[k]) for k in params}
