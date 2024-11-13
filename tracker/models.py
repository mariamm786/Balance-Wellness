from django.db import models
from django.contrib.auth.models import User
import uuid

class SymptomLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=100)
    severity = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.symptom} - Severity: {self.severity}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="received_messages")
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject


