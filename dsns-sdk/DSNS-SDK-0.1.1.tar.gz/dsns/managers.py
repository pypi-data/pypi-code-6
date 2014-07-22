from django.db import models


class ChannelManager(models.Manager):
    """
    Channel Manager to manager channels
    if new channel is being created then will also
    create same channel to DSNS server and in case failure
    happens then raises exception:
        ValidationError
    """
    pass
