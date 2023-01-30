from django.db import models

class PNRStatusModel(models.Model):
    pnr_number = models.TextField(max_length = 10)
    pnr_status = models.TextField()

    def __str__(self):
        return self.pnr_number