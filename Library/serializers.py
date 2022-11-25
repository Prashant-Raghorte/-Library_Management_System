from rest_framework import serializers
from . models import Book
from . models import Student
from . models import IssuedBook
from . models import Penalty
from . models import Teacher
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        #fields = ['name','author','isbn','category']
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        #fields = ['user','classroom','branch','roll_no','phone','image']
        fields = "__all__"


class IssuedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedBook
        #fields = ['student_id','isbn','issued_date','expiry_date']
        fields = "__all__"

class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalty
        #fields = ['student_id','isbn','issued_date','expiry_date']
        fields = "__all__"

class IssueBookAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedBook
        #fields = ['student_id','book_id']
        fields = "__all__"

class PenaltyAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedBook
        #fields = ['student_id','book_id']
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        #fields = ['user','classroom','branch','roll_no','phone','image']
        fields = "__all__"
