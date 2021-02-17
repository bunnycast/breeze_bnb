from django.db import models


class TimeStampedModel(models.Model):
    """ Time Stamped Model """

    created_at = models.DateTimeField()
    updated_at = models.DateTimeFieldField()

    class Meta:
        abstract = True
