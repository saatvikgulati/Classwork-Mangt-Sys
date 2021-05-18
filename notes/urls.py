from django.urls import path
from . import views
urlpatterns = [
    path('faculty-notes/',views.faculty_notes,name="faculty-notes"),
    path('create/',views.create_notes,name="create-notes"),
    path('subject-table-student-notes/',views.subject_table_student_notes,name="subject-table-student-notes"),
    path('student-notes/<int:id>/',views.student_notes,name='student-notes'),
    path('update-notes/<int:id>/',views.update_notes,name='update-notes'),
    path('delete-notes-confirm/<int:id>/',views.delete_notes_confirm,name='delete-notes-confirm'),
    path('delete-notes/<int:id>/',views.delete_notes,name='delete-notes'),
]
