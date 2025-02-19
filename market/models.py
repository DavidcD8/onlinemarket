from django.db import models


# Choices for the condition of the item
Condition = (
       ('New', 'New'),
       ('Used', 'Used')

)

# Model for items
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    images = models.ImageField(upload_to='images/')
    price = models.FloatField()
    condition = models.CharField(max_length=4, choices=Condition)

    def __str__(self):
        return self.name
