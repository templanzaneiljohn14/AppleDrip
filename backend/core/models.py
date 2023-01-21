from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

def image_path(instance, filename):
    return 'posts/{filename}'.format(filename=filename)

class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    content = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_path, default='posts/image.jpg')
    created_at = models. DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserGallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    image = models.ImageField(upload_to=image_path, default='posts/image.jpg')
    created_at = models. DateTimeField(auto_now_add=True)

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    message = models.BinaryField()
    sent_at = models. DateTimeField(auto_now_add=True)


class UserFollowers(models.Model):
    follow_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    follower_id = models.IntegerField()


class UserFriends(models.Model):
    frnd_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    friend_id = models.IntegerField()
    status = models.IntegerField(default=0, editable=True)


class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=255)
    created_at = models. DateTimeField(auto_now_add=True)


class GroupMembers(models.Model):
    gm_id = models.AutoField(primary_key=True)
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    joined_at = models. DateTimeField(auto_now_add=True)


class GroupPosts(models.Model):
    gp_id = models.AutoField(primary_key=True)
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    content = models.BinaryField()
    created_at = models. DateTimeField(auto_now_add=True)

class EmailCode(models.Model):
    code_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    email_code = models.CharField(max_length=6)
    sent_at = models.DateTimeField(auto_now_add=True)
