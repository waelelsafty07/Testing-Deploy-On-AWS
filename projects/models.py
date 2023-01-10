from django.db import models
from django.utils import timezone
from users.models import Users
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.


class Projects(models.Model):  # table
    name = models.CharField(max_length=100, default='New Project')
    creation_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='files')
    image_thumbnail = ImageSpecField(source='image', processors=[
                                     ResizeToFill(100, 100)], format='JPEG', options={'quality': 90})

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects'
        indexes = [models.Index(
            fields=['name'], name='name_projects_index')]
