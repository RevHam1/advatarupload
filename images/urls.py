from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('load_image', views.load_image),
    path('survey', views.survey),
    # path('result', views.result),

    # path('upload_form', views.upload_form),

    path("edit_img/<int:img_id>", views.edit_img),
    # path("reset_img/<int:img_id>", views.reset_img),

    path("delete_user/<int:user_id>", views.delete_user),
    # path("delete_user", views.delete_user)

    # path('user_img/<int:user_id>', views.user_image),
]

