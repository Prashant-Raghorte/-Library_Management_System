from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + "-------" + str(self.id)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return str(self.id) + "----" + self.user.username


def expiry():
    print(f"28----------------------{datetime.today() + timedelta(days=14)}")
    return datetime.today() + timedelta(days=14)

class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued = models.BooleanField(default=False)
    issued_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(auto_now=False, auto_created=False, auto_now_add=False, null=True, blank=True)
    expiry_date = models.DateTimeField(default=expiry)

    def __str__(self):
        return str(self.id) +"----"+ str(self.book.name) + "----" + str(self.student.user.username)

def penalty_expiry_calculation():
    return datetime.now() + timedelta(days=30)

class Penalty(models.Model):
    issue_details = models.ForeignKey(IssuedBook, on_delete=models.CASCADE,null=True,blank=True)
    penalty_expiry = models.DateTimeField(default=penalty_expiry_calculation)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + "------"+str(self.issue_details.student.user.username) + "-----" + str(self.is_paid)

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=100)
    classroom = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return str(self.id) + "----" + self.first_name + "-----" + self.last_name
