from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

class User(AbstractUser):
    friends = models.ManyToManyField('self', symmetrical=False, related_name='user_friends', blank=True)

    groups = models.ManyToManyField(Group, related_name='friends_accounts_app_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='friends_accounts_app_users', blank=True)

    def add_friend(self, friend):
        if not self.is_friends_with(friend):
            self.friends.add(friend)
            friend.friends.add(self)

    def remove_friend(self, friend):
        if self.is_friends_with(friend):
            self.friends.remove(friend)
            friend.friends.remove(self)

    def is_friends_with(self, friend):
        return self.friends.filter(id=friend.id).exists()

    def __str__(self):
        return self.username


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    hidden_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Account"
