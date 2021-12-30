from django.db import models
from users.models import User


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
