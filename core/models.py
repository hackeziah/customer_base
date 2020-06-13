from django.db import models
from django.utils import timezone

now = timezone.now()

class Profession(models.Model):
    description = models.CharField(max_length = 50)

    @property
    def __str__(self):
        return self.description
class DataSheet(models.Model):
    description = models.CharField(max_length = 50)
    historical_data = models.TextField()

    def __str__(self):
        return self.description
class Customer(models.Model):
    name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 50)
    profession = models.ManyToManyField(Profession)
    data_sheet = models.OneToOneField(DataSheet, on_delete=models.CASCADE, null = True, blank = True)
    active = models.BooleanField(default=True)
    cu_number = models.CharField(max_length = 12,unique = True,null = True, blank = True)

    #for setting up status active more details
    @property
    def status_message(self):
        if self.active:
            return "Customer is Active"
        else:
            return "Customer is Not Active"

    def num_professions(self):
        return self.profession.all().count()

    def __str__(self):
        return self.name

class Document(models.Model):
    PP = 'PP'
    ID = 'ID'
    OT = 'OT'

    DOC_TYPE = (
        (PP, 'Passport'),
        (ID, 'Identity Card'),
        (OT, 'Others'),
    )

    dtype  = models.CharField(choices = DOC_TYPE,max_length= 2)
    doc_number = models.CharField(max_length = 50)
    customer  = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_number
