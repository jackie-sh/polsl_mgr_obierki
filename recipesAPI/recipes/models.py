from django.db import models
from users.models import User


class RecipeImage(models.Model):
    file = models.ImageField(blank=True)

    def __str__(self):
        return self.file.name


class RecipeCategory(models.Model):
    name = models.CharField(max_length=30)


class RecipeImage(models.Model):
    file = models.ImageField()

    def __str__(self):
        return self.file.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=30, default="")
    content = models.CharField(max_length=1000, default="")
    shortDescription = models.CharField(max_length=100, default="")
    category = models.ForeignKey(RecipeCategory, on_delete=models.PROTECT)
    mainImage = models.ForeignKey(RecipeImage, on_delete=models.CASCADE, related_name="image")
    view_count = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.title

    class Meta:
        ordering = ['create_date', 'view_count']


class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    commentText = models.CharField(max_length=300)
    rating = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.create_date, self.rating)

    class Meta:
        ordering = ['create_date']


class Message(models.Model):
    message = models.CharField(max_length=300)
    pub_date = models.DateField()
    senderID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiverID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    def __str__(self):
        return "%s %s %s" % (self.message, self.senderID, self.receiverID)

    class Meta:
        ordering = ['message', 'pub_date']
