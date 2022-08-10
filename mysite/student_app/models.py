# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_teacher=None, is_student=None):
        """
        Creates and saves a User with the given email, mobile, gender and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

    
        user = self.model(
            email=self.normalize_email(email)
,
            is_teacher=is_teacher,
            is_student=is_student,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
        

    def create_superuser(self, email, password=None, is_teacher=None, is_student=None):
        """
        Creates and saves a superuser with the given email, mobile, gender and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            is_teacher=is_teacher,
            is_student=is_student,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    is_teacher=models.BooleanField(default="", blank=True, null=True)
    is_student=models.BooleanField(default="", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'is_teacher', 'is_student']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Teacher(models.Model):
    user=models.ForeignKey(User, related_name='user_teacher', on_delete=models.CASCADE)
    fullname=models.CharField(max_length=255)
    contact=models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    city=models.CharField(max_length=255)


class Student(models.Model):
    user=models.ForeignKey(User, related_name='user_student', on_delete=models.CASCADE)
    fullname=models.CharField(max_length=255)
    contact=models.CharField(max_length=255)
    student_class = models.CharField(max_length=255)
    city=models.CharField(max_length=255)

class Result(models.Model):
    total=models.IntegerField(default=0)
    is_pass=models.CharField(max_length=255)
    percentage=models.CharField(max_length=255)    

class Marks(models.Model):
    usersmrk=models.ForeignKey(Student, related_name='usersmrk_marks', on_delete=models.CASCADE)
    subject1=models.CharField(max_length=255)
    subject2=models.CharField(max_length=255)
    subject3=models.CharField(max_length=255)
    subject4=models.CharField(max_length=255)
    subject5=models.CharField(max_length=255)
    userstd=models.ForeignKey(Result, related_name='userstd_result', on_delete=models.CASCADE, blank=True, null=True, default=None)

    
    
    
