from django.contrib.auth.models import User
from django.db import models


class ChurchOperator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_key_keeper = models.BooleanField(default=False)
    is_bell_ringer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class BellMovementRequest(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("REJECTED", "Rejected"),
        ("APPROVED", "Approved"),
    )

    requester = models.ForeignKey(
        ChurchOperator,
        on_delete=models.CASCADE,
        related_name="requested_bell_movements",
    )
    destination_church = models.CharField(max_length=100)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Movement request from {self.requester.user.username} to {self.destination_church}"


class BellMovementApproval(models.Model):
    request = models.OneToOneField(
        BellMovementRequest, on_delete=models.CASCADE, related_name="approval"
    )
    operator = models.ForeignKey(ChurchOperator, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Approval for request {self.request.id} by {self.operator.user.username}"
        )


class Report(models.Model):
    creator = models.ForeignKey(
        ChurchOperator, on_delete=models.CASCADE, related_name="created_reports"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
