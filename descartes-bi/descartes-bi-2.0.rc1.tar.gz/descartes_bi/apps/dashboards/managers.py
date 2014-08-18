from django.db import models


class DashboardElementManager(models.Manager):
    def enabled(self):
        return self.filter(enabled=True)
