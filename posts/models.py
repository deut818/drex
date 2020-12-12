from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts_created", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", blank=True)
    video = models.FileField(upload_to="videos/%Y/%m/%d/", blank=True)
    audio = models.FileField(upload_to="audio/%Y/%m/%d/", blank=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="posts_liked", blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # class Meta:
    #     ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:detail', args=[self.id, self.slug])

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments_made", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return "Comment by {} on {}".format(self.user.fname, self.post)

class CommentReply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="replies_to_comments", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="replies", on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return "Reply by {} to {}".format(self.user, self.comment)