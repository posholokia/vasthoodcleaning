from apps.clients.models.orm import CustomerModel
from apps.jobs.models.entity import (
    JobEntity,
    JobStatus,
)
from django.db import models


class JobModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True, unique=True)
    schedule = models.DateTimeField(null=True)
    address = models.CharField(max_length=256)
    status = models.CharField(max_length=32)
    total_cost = models.IntegerField()
    paid = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(
        CustomerModel,
        on_delete=models.CASCADE,
        related_name="jobs",
    )

    def to_entity(self) -> JobEntity:
        return JobEntity(
            id=self.id,
            schedule=self.schedule,
            address=self.address,
            status=JobStatus(self.status),
            total_cost=self.total_cost,
            paid=self.paid,
            last_updated=self.last_updated,
        )
