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
    price = models.FloatField()
    condition = models.CharField(max_length=4, choices=Condition)

    def __str__(self):
        return self.name


# Model for item images
class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.item.name