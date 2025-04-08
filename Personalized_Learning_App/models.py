from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    topic = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} - {self.topic} ({self.created_at.strftime('%Y-%m-%d')})"


class TestSubmission(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return f"Submission by {self.user.username} for {self.test.topic} on {self.submitted_at.strftime('%Y-%m-%d')}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.name} - {self.email}"

