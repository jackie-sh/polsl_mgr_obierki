from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s" % self.name

    class Meta:
        ordering = ['name', 'email']


class Rating(models.Model):
    comments = models.CharField(max_length=300)
    rating = models.IntegerField()
    pub_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.comments, self.rating)

    class Meta:
        ordering = ['comments', 'pub_date']


class Message(models.Model):
    message = models.CharField(max_length=300)
    pub_date = models.DateField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    def __str__(self):
        return "%s %s %s" % (self.message, self.sender, self.receiver)

    class Meta:
        ordering = ['message', 'pub_date']


class Recipe(models.Model):
    description = models.CharField(max_length=300)
    recipe_type = models.CharField(max_length=30)
    views = models.IntegerField()
    rating = models.ManyToManyField(Rating)

    def __str__(self):
        return "%s %s %s" % (self.description, self.views, self.recipe_type)

    class Meta:
        ordering = ['recipe_type', 'views']
