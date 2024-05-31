from django.urls import path
from .views import profile_view, register,edit_profile, timeline_view, complete_stage
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('register/', register, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('login/', LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('timeline/', timeline_view, name='timeline'),
    path('complete_stage/<int:stage_id>/', complete_stage, name='complete_stage'),
    
]

#path('', timeline2_view, name='timeline2'),