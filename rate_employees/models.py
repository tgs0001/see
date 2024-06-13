from django.db import models

# Create your models here.

class Employee(models.Model):
    empid = models.IntegerField()
    enothi_id = models.CharField(max_length=40)
    ename = models.CharField(max_length=40)
    eemail = models.EmailField(max_length=30)
    edesignation = models.CharField(max_length=40)
    edept = models.CharField(max_length=40)
    esection = models.CharField(max_length=40)
    edivision = models.CharField(max_length=40, default='null_div')
    edirectorate = models.CharField(max_length=40)
    

    def setEname(self,ename):
        self.ename = ename


class Evaluation(models.Model):
    evaluateeid = models.IntegerField()
    evaluatorid = models.IntegerField()
    secDeptEv = models.IntegerField(default=None)
    commEv = models.IntegerField(default=None)
    behavEv = models.IntegerField(default=None)
    comid = models.IntegerField(default=None)


class Designation(models.Model):
    desigid = models.IntegerField()
    designame = models.CharField(max_length=40)
    desigshortname = models.CharField(max_length=40)