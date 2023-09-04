from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from .models import Profile, User
@receiver(post_save, sender=User)
def profile_update(sender, instance, created, **kwargs):
    print('User signal!')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )

@receiver(post_save, sender=Profile)
def update_user(sender,instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created is False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

@receiver(post_delete, sender=Profile)
def profile_delete(sender, instance, **kwargs):
    user = instance.user
    user.delete()