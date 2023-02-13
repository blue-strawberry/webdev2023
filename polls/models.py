from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    def get_absolute_url(self):
        return reverse('polls:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Pub')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class ingredientItem(models.Model):
    productName = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    size = models.CharField(max_length=20, null='small')
    unitPrice = models.DecimalField(max_digits=19, decimal_places=2)
    img_url = models.TextField()

    def __str__(self):
        return str(self.productName)


class Recipe(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  img_url = models.TextField()

  def get_absolute_url(self):
      return reverse("recipes-detail", kwargs={"pk": self.pk})

  def __str__(self):
    return self.title