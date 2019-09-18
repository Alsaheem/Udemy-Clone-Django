from django.db import models
from memberships.models import Membership
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=150)

    def __str__(self):
        return '{}'.format(self.category)

class Course(models.Model):
    creator = models.ForeignKey(User,on_delete = models.CASCADE)
    slug = models.SlugField()
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField(max_length=400)
    created_time = models.DateTimeField(auto_now=True)
    duration = models.CharField(max_length=10,help_text = 'please use the following formats : 1 Week or 1 Month')
    starting_date = models.DateField(null=True)
    ending_date = models.DateField(null=True)
    allowed_memberships = models.ManyToManyField(Membership,related_name='membershipsallowed')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"slug": self.slug})

    def get_courses_related_to_memberships(self):
        return self.courses.all()

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')

class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=30)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    video_url = models.FileField(upload_to='videos/', null=True)
    thumbnail = models.ImageField()
    position = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:lesson_detail", kwargs={"course_slug": self.course.slug,'lesson_slug':self.slug})
