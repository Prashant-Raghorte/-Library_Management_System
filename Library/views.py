from Library.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required

# REST API
from django.http import  HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .models import Student
from .models import IssuedBook
from .models import Teacher
from Library.serializers import *
from rest_framework import status
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from Library.pagination import *


# Create your views here.
class BookList(APIView):
    def get(self,request):
        book1 =Book.objects.all()
        serializer = BookSerializer(book1, many=True)
        return Response(serializer.data)

class IssueBookAPIView(APIView):
    def post(self,request):
        print(type(request.data))
        student_id = request.data.get('student_id')
        book_id = request.data.get('book_id')
        student_obj = Student.objects.get(id=student_id)
        book_obj = Book.objects.get(id=book_id)
        issue_obj = IssuedBook.objects.create(student=student_obj, book=book_obj, )
        return Response({"message":"success"})
        


class PenaltyAPIView(APIView):
    def get(self,request):
        student_id = request.data.get('student_id')
        book_id = request.data.get('book_id')
        print("student_id :", student_id)
        student_obj = Student.objects.get(id=student_id)
        book_obj = Book.objects.get(id=book_id)
        issue_obj = IssuedBook.objects.filter(student=student_obj,book=book_obj,returned=False).last()
        print(f"54--------{issue_obj}----------{issue_obj}-----------{datetime.today()}")
        day_today = datetime.now()
        import pytz
        utc = pytz.UTC
        is_penalty=False
        print(f'72--------------{issue_obj}')
        if issue_obj:
            issue_date = issue_obj.issued_date
            expi_date = issue_obj.expiry_date
            print(issue_date)
            day_today1 = utc.localize(day_today)
            # expi_date1 = utc.localize(expi_date)
            if day_today1 > expi_date:                
                time_result = day_today1 - expi_date
                print(f'70--------------{time_result.days}')
                if time_result.days > 0:
                    print(f'70--------------{time_result.days}')
                    fine = 0
                    #day = 0
                    fine = time_result.days * 10
                    print("76----------{fine}")
                    penalty_obj = Penalty.objects.create(issue_details=issue_obj,amount=fine)
                    serialized_data=PenaltySerializer(penalty_obj).data
                    is_penalty = True
                    issue_obj.returned = True
                    issue_obj.save()
                    res = {"status":"success",
                    "penalty":is_penalty,
                    "data":serialized_data}
                    return Response(res, status=status.HTTP_200_OK)

                issue_obj.returned = True
                issue_obj.save()
                serialized_data=IssuedBookSerializer(issue_obj).data
                is_penalty=False
                res = {"status":"success",
                    "penalty":is_penalty,
                    "data":serialized_data}
                return Response(res, status=status.HTTP_200_OK)
                
            issue_obj.returned = True
            issue_obj.save()
            serialized_data=IssuedBookSerializer(issue_obj).data
            is_penalty=False
            res = {"status":"success",
                    "penalty":is_penalty,
                    "data":serialized_data}
            return Response(res, status=status.HTTP_200_OK)
        res = {"status":"fail",
                    "penalty":is_penalty,
                    "data":[],
                    "message":"There is no record found with thid details"}
        return Response(res, status=status.HTTP_200_OK)




class StudentList(APIView):
    def get(self,request):
        student1 =Student.objects.all()
        serializer = StudentSerializer(student1, many=True)
        return Response(serializer.data)

    def post(self):
        pass

class IssuedBookList(APIView):
    def get(self,request):
        IssuedBook1 =IssuedBook.objects.all()
        serializer = IssuedBookSerializer(IssuedBook1, many=True)
        return Response(serializer.data)

    def post(self):
        pass

def PenaltyList(APIVIEW):
    def get(self, request):
        Penalty = Penalty.objects.all()
        serializer = PenaltySerializer(Penalty, many=True)
        return Response(serializer.data)




#ViewSet Class
# class TeacherViewSet(ViewSet): 
#     def list(self,request):
#         print(f"139------{self.action}")
#         teacher_obj = Teacher.objects.all()
#         serializer = TeacherSerializer(teacher_obj, many = True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk):
#         print(f"145------{self.action}")
#         id = pk 
#         if id is not None:  
#             teacher_obj = Teacher.objects.get(id=pk)
#             serializer = TeacherSerializer(teacher_obj)
#             return Response(serializer.data)
#         return Response({'msg':'Data Retrieve'})

#     def create(self,request):
#         print(f"154------{self.action}")
#         serializer = TeacherSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'Data Created'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self,request, pk):
#         print(f"162------{self.action}")
#         id = pk 
#         teacher_obj = Teacher.objects.get(id=pk)
#         serializer = TeacherSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'Data Updated'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self,request, pk):
#         print(f"172------{self.action}")
#         id = pk 
#         teacher_obj = Teacher.objects.get(id=pk)
#         serializer = TeacherSerializer(teacher_obj, data = request.data, partial =True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'Partial Data Updated'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk):
#         print(f"182------{self.action}")
#         id = pk
#         teacher_obj = Teacher.objects.get(id=pk)
#         teacher_obj.delete()
#         return Response({'msg':'Data Deleted'})

#ModelViewSet
class TeacherModelViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = LimitOffsetPagination




def index(request):
    return render(request, "index.html")

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category)
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert})
    return render(request, "add_book.html")

@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books':books})

@login_required(login_url = '/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})

@login_required(login_url = '/admin_login')
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            alert = True
            return render(request, "issue_book.html", {'obj':obj, 'alert':alert})
    return render(request, "issue_book.html", {'form':form})

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        books = list(models.Book.objects.filter(isbn=i.isbn))
        students = list(models.Student.objects.filter(user=i.student_id))
        i=0
        for l in books:
            t=(students[i].user,students[i].user_id,books[i].name,books[i].isbn,issuedBooks[0].issued_date,issuedBooks[0].expiry_date,fine)
            i=i+1
            details.append(t)
    return render(request, "view_issued_book.html", {'issuedBooks':issuedBooks, 'details':details})

@login_required(login_url = '/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(isbn=i.isbn)
        for book in books:
            t=(request.user.id, request.user.get_full_name, book.name,book.author)
            li1.append(t)

        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>15:
            day=d-14
            fine=day*5
        t=(issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)
    return render(request,'student_issued_books.html',{'li1':li1, 'li2':li2})

@login_required(login_url = '/student_login')
def profile(request):
    return render(request, "profile.html")

@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert':alert})
    return render(request, "edit_profile.html")

def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/view_books")

def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    return redirect("/view_students")

def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "change_password.html")

def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "student_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Student.objects.create(user=user, phone=phone, branch=branch, classroom=classroom,roll_no=roll_no, image=image)
        user.save()
        student.save()
        alert = True
        return render(request, "student_registration.html", {'alert':alert})
    return render(request, "student_registration.html")

def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "student_login.html", {'alert':alert})
    return render(request, "student_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

def Logout(request):
    logout(request)
    return redirect ("/")