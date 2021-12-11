from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s" % self.name

    class Meta:
        ordering = ['name', 'email']


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    comments = models.CharField(max_length=300)
    rating = models.IntegerField()
    pub_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=300)
    recipe_type = models.CharField(max_length=30)
    views = models.IntegerField()
    rating = models.ManyToManyField(Rating)
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return "%s %s %s %s" % (self.description, self.views, self.recipe_type, self.file)

    class Meta:
        ordering = ['recipe_type', 'views']