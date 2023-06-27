from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'User'


urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('insurance/', views.InsuranceView.as_view()),
    path('api-token-auth/', obtain_auth_token),
    path('get-info/', views.GetInfoView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]
