from django.db import models


class Customers(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(blank=False)
    transaction_code = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name

    def _get_first_name(self):
        first_name = self.name.split()[0]
        first_name = first_name.capitalize()
        return first_name

    first_name = property(_get_first_name)
