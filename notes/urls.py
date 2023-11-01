from django.urls import path

from . import views

urlpatterns = [
    path('', views.NoteList.as_view(), name='note_list'),
    path('shared-with-me/', views.SharedNoteWithMeDetail.as_view(), name='shared_with_me_detail'),
    path('<note_id>/', views.NoteDetail.as_view(), name='note_detail'),
    path('<note_id>/share-with/', views.ShareNoteWithDetail.as_view(), name='share_with_detail'),
]
