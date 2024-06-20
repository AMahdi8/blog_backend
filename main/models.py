from datetime import datetime
from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class CustomUser(AbstractUser):
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=11)
    about_me = models.TextField()
    profile = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.username


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_published:
            self.publish_date = datetime.now()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return f'{self.user} -> {self.title}'


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    reply = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, related_name='comment_comments', blank=True, null=True)
    body = models.TextField()
    is_reply = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if self.reply:
            return f'{self.user} -> {self.reply} -> {self.post}'
        return f'{self.user} -> {self.post}'


class Like(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self) -> str:
        return f'{self.user} liked {self.post}'


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class PostTag(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name='tages')


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.follower} followed {self.followed}'


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='sent_messages')
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='received_messages')
    reply = models.ForeignKey(
        'Message', on_delete=models.PROTECT, related_name='replies', blank=True, null=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.sender} messaged: "{self.message}."  to {self.receiver}'
