from django.db import models


class Catagories(models.Model):
    name = models.CharField(max_length=50, blank=False)

    @staticmethod
    def get_all_catagories():
        return Catagories.objects.all()

    def __str__(self):
        return self.name
