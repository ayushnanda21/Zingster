from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#Use of signals
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to ='uploads/post_photos', blank= True , null = True)
    created_on = models.DateTimeField(default = timezone.now)
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,blank= True, related_name = 'likes')
    dislikes = models.ManyToManyField(User,blank= True, related_name = 'dislikes')


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,blank= True, related_name = 'comments_likes')
    dislikes = models.ManyToManyField(User,blank= True, related_name = 'comments_dislikes')
    parent = models.ForeignKey('self',on_delete =models.CASCADE ,blank = True,null= True, related_name='+')

    @property
    def children(self):
        return Comment.objects.filter(parent = self ).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


class UserProfile(models.Model):
    user  = models.OneToOneField(User,  primary_key = True , verbose_name = 'user', related_name ='profile' ,on_delete=models.CASCADE)
    name =models.CharField(max_length=30, blank = True , null =True)
    bio = models.TextField(max_length = 500, blank = True, null = True)
    birth_date  = models.DateField(null =True,blank= True)
    location = models.CharField(max_length = 100, blank = True, null = True)
    picture= models.ImageField(upload_to= 'uploads/profile_pictures', default ="uploads/profile_pictures/default.png",blank = True)
    #followers
    followers = models.ManyToManyField(User, blank =True , related_name = 'followers')


# SIGNALS USE for auto profile creation once user is created
@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, created, **kwargs):
    instance.profile.save()

#model for notifications:
class Notification(models.Model):
	notification_type = models.IntegerField()
	to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
	from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	user_has_seen = models.BooleanField(default=False)
