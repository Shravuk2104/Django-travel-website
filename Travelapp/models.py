from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class package(models.Model):
    name=models.CharField(max_length=50,verbose_name="Package name")
    price=models.FloatField()
    pdetails=models.CharField(max_length=150,verbose_name="Package Details")
    CAT=((1,"By Plane"),(2,"By Train"),(3,"By Bus"))
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    from_date = models.DateField()  # Date field for the booking start date
    to_date = models.DateField()
    pimage=models.ImageField(upload_to='image')


    def __str__(self):
        return self.name
    

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(package,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)


class ConfirmBooking(models.Model):
    B_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(package,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
