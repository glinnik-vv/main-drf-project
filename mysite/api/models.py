from ast import mod
from unittest import result
from django.db import models
from django.contrib.auth.models import User
from sqlalchemy import ForeignKey


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    settings = models.JSONField()

    def __str__(self):
        return self.user


class Lpu(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    unigate_login = models.CharField(max_length=255)
    unigate_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    id_pac = models.CharField(max_length=100)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10)
    snils = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.surname}"
    

class Direction(models.Model):
    promed_id = models.BigIntegerField(unique=True)
    promed_num = models.CharField(max_length=250)
    insert_date = models.DateTimeField()
    update_date = models.DateTimeField()
    send_status = models.IntegerField()
    lpu = models.ForeignKey(Lpu, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    receive_status = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class OrderInfo(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    service_code = models.CharField(max_length=250)
    service_name = models.CharField(max_length=250)
    order_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Measurement(models.Model):
    measurement_code = models.CharField(max_length=250)
    measurement_name = models.CharField(max_length=250)
    promed_code = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Results(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    service_code = models.CharField(max_length=250)
    service_name = models.CharField(max_length=250)
    result_date = models.DateTimeField()
    result_text = models.CharField(max_length=250)
    result_value = models.CharField(max_length=250)
    promed_code = models.CharField(max_length=250)
    promed_result = models.CharField(max_length=250)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UploadFile(models.Model):
    file = models.FileField()
    service_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file
