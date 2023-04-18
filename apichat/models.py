from django.db import models
import time

class ChatMessage(models.Model):
    prompt = models.TextField ()
    response = models.TextField ()
    nonce = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.nonce:
            self.nonce = int(time.time())
        super(ChatMessage, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.prompt} - {self.response}'
