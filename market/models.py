from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




# Model for User
class User(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.name

    # Signal to create user profile when a User is created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # Signal to save user profile when a User is saved
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


# Model for items
class Item(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    is_sold = models.BooleanField(default=False)  # Ensure this field exists


    def save(self, *args, **kwargs):
        # Prevent changing the seller after creation
        if self.pk and self.seller_id != Item.objects.get(pk=self.pk).seller_id:
            raise ValidationError("You cannot change the seller of an item.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



# Model for item images
class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.item.name


