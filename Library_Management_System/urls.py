from django.urls import path, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from Library import views
from rest_framework.routers import DefaultRouter

#creating Rounter Obj
router = DefaultRouter()

#Register  TeacherViewSet with Router
router.register(r'teacher', views.TeacherModelViewSet, basename='teacher')

# user_list = views.TeacherViewSet.as_view({'get': 'list'})
# user_detail = views.TeacherViewSet.as_view({'get': 'retrieve'})
# user_create = views.TeacherViewSet.as_view({'Post': 'create'})
# user_update = views.TeacherViewSet.as_view({'PUT': 'update'})
# user_partial_update = views.TeacherViewSet.as_view({'PATCH': 'partial_update'})
# user_delete = views.TeacherViewSet.as_view({'delete': 'delete'})



urlpatterns = [
    #path("", views.index, name="index"),
    path('admin/', admin.site.urls),

    path(r'Book/', views.BookList.as_view()),
    path(r'Student/', views.StudentList.as_view()),
    path(r'IssuedBook/', views.IssuedBookList.as_view()),
    path("book/issue", views.IssueBookAPIView.as_view(), name="issue-book"),
    path("book/penalty", views.PenaltyAPIView.as_view(), name="book-penalty"),
    path("",include(router.urls)),


    path("add_book/", views.add_book, name="add_book"),
    path("view_books/", views.view_books, name="view_books"),
    path("view_students/", views.view_students, name="view_students"),
    path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

    path("student_registration/", views.student_registration, name="student_registration"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout, name="logout"),

    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
]