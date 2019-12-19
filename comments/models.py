from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.template.defaultfilters import date
from django.utils.translation import ugettext as _
from django.utils.timezone import localtime
from django.contrib.auth.models import User


class Dialog(TimeStampedModel):
    from_user = models.ForeignKey(User, related_name="dialog_owner",on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # last_message = models.OneToOneField("Message", related_name="last_message_of", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return _("Chatting with ") + self.to_user.username
    
    def get_formatted_modified_datetime(self, str):
        return date(localtime(self.modified), str)


class Message(TimeStampedModel, SoftDeletableModel):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)

    def get_formatted_create_datetime(self, str): #"D d M Y"
        return date(localtime(self.created), str)

    def __str__(self):
        return self.sender.username + "(" + self.get_formatted_create_datetime() + ") - '" + self.text + "'"
