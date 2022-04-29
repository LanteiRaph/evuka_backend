from django.db import models

# Create your models here.
# TODO:Comment the code below....
from decimal import Decimal
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from .helpers import get_timer
from django.db.models import Count
from mutagen.mp4 import MP4, MP4StreamInfoError

from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary_storage.validators import validate_video

from cloudinary.models import CloudinaryField

# Represnts the business logic of the application


#Reprsent a topic:Undestood as the category of diffrent courses e.g['Python', 'web development']
class Topic(models.Model):
    topic = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    image = models.ImageField(upload_to='topic_images',storage=MediaCloudinaryStorage(), null=True)
    related_cousres = models.ManyToManyField('Course', blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'topic'

    def get_absolute_url(self):
        return self.image_url.url


class Course(models.Model):

    course = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # category = models.ForeignKey('Categorys', on_delete=models.CASCADE)
    comment = models.ManyToManyField('Comment', blank=True)
    sections = models.ManyToManyField('Section', blank=True)

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    image_url = models.ImageField(upload_to='course_images',storage=MediaCloudinaryStorage())
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    class Meta:
        db_table = 'course'

    def get_brief_description(self):
        return self.description[:100]

    def get_enrolled_students(self):
        students = get_user_model().objects.all().filter(paid_courses=self)
        return len(students)

    def get_total_lectures(self):
        lectures = 0

        for section in self.sections.all():
            lectures += len(section.episodes.all())

        return lectures

    def get_total_length(self):
        length = Decimal(0.0)

        for section in self.sections.all():
            for episode in section.episodes.all():
                length += episode.length

        return get_timer(length, type='short')

    def get_absolute_url(self):
        return self.image_url.url


class Section(models.Model):

    section = models.AutoField(primary_key=True)
    episodes = models.ManyToManyField('Episode', blank=True)
    title = models.CharField(max_length=255)
    descrption = models.CharField(max_length=255)
    total_episodes = models.IntegerField(blank=True, null=True)
    total_length = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = 'section'

    def get_total_episodes(self):

        return self.episodes.all().count

    def get_total_length(self):

        total = Decimal(0.0)

        for episode in self.episodes.all():
            total += episode.length

        return get_timer(total, type='min')


class Episode(models.Model):

    episode = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    file=CloudinaryField(resource_type='video',validators=[validate_video],folder='media')
    # file = models.FileField(upload_to='course_videos')
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'episode'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return self.file.url

    def get_length(self):
        try:
            video = MP4(self.file)
            return video.info.length
        except MP4StreamInfoError:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)

    def save(self, *args, **kwargs):
        self.length = self.get_length()
        return super().save(*args, **kwargs)


class Comment(models.Model):

    comment = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    msg = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment'

    def __str__(self) -> str:
        return self.msg
