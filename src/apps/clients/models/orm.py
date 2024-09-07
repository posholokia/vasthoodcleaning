from django.db import models


class CustomerModel(models.Model):
    # в CRM может быть много кастомеров с одинаковыми телефонами,
    # отличающиеся адресом, именем и т.п
    id = models.CharField(max_length=64, primary_key=True, unique=True)
    phone = models.CharField(max_length=16, db_index=True)

