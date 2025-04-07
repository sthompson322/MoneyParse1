from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SecurityAnswers(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    securityAnswer1 = models.CharField(max_length=255, null=True, blank=True)
    securityAnswer2 = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.securityAnswer1 + self.securityAnswer2