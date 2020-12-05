from django.db import models
from utils.model import BaseModel

# Create your models here.
class ActivityLog(BaseModel) : 
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    content = models.TextField("내용", null=True, blank=True)
    exp = models.IntegerField("경험치", null=True, blank=True)
 