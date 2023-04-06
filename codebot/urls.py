from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('register/', views.register_user, name='register'),
	path('past', views.past, name='past'),
	path('delete_past/<Past_id>', views.delete_past, name='delete_past'),
	path('forgot_password/', views.password_reset, name='password_reset'),
    path('forgot_password/<str:id>/', views.password_reset_verified,
         name='password_reset_verified'),


]
