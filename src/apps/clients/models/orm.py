from django.db import models


class CustomerModel(models.Model):
    """
    Модель кастомера. id присваивается такой же, как в CRM.
    """

    id = models.CharField(max_length=64, primary_key=True, unique=True)
    phone = models.CharField(max_length=16, db_index=True)
