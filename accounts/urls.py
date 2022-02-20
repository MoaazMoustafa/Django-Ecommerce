from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm
app_name = 'account'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activate/<slug:uidb64>/<slug:token>',
         views.activate_account, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registeration/login.html',
         form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'),  name='logout'),
    path('profile/edit/', views.profile_edit,  name='profile_edit'),

]
