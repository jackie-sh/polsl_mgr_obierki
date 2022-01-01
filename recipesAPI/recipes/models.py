from django.db import models
from users.models import User

class RecipeImage(models.Model):
    file = models.ImageField(blank=True) #TODO until file upload complete this is tru

class RecipeCategory(models.Model):
    name = models.CharField(max_length=30)

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=30, default="")
    content = models.CharField(max_length=1000, default="")
    shortDescription = models.CharField(max_length=100, default="")
    category = models.ForeignKey(RecipeCategory, on_delete=models.PROTECT)
    mainImage = models.ForeignKey(RecipeImage, on_delete=models.SET_NULL, null=True)

    view_count = models.IntegerField()

    def __str__(self):
        return "%s" % self.title

    class Meta:
        ordering = ['view_count']


class Rating(models.Model):
    comments = models.CharField(max_length=300)
    rating = models.IntegerField()
    pub_date = models.DateField(auto_created=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.comments, self.rating)

    class Meta:
        ordering = ['comments', 'pub_date']

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=300)
    pub_date = models.DateField()
    senderID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiverID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    def __str__(self):
        return "%s %s %s" % (self.message, self.senderID, self.receiverID)

    class Meta:
        ordering = ['message', 'pub_date']
