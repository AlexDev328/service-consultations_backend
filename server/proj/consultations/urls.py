from django.urls import path

from .views import UserProfileListCreateView, \
    UserProfileDetailView, create_application, aprove_application, ConsultationView, auth_by_link

urlpatterns = (
    path("all-profiles", UserProfileListCreateView.as_view(), name="all-profiles"),
    path("myprofile/", UserProfileDetailView.as_view(), name="profile"),
    path("profile/<int:pk>", UserProfileDetailView.as_view(), name="profile"),
    path("consultations", ConsultationView.as_view({'get': 'list', 'post':'create', 'put':'update', 'patch':'partial_update'})),
    path("consultations/<int:pk>", ConsultationView.as_view({'get': 'retrieve',  'put':'update', 'patch':'partial_update'})),
    path('prepare_room', create_application, name='Создать комнату'),
    path('auth_by_link/<str:auth_code>', auth_by_link, name = "Авторизация по ссылке"),
    path('aprove_application/<int:id>', aprove_application, name='Создать комнату')
)