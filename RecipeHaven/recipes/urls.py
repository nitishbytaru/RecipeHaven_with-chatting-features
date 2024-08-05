from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("create_recipe/", views.recipe_create, name="create_recipe"),
    path("<int:recipe_id>/edit_recipe/", views.edit_recipe, name="edit_recipe"),
    path("<int:recipe_id>/delete_recipe/", views.delete_recipe, name="delete_recipe"),
    path("<int:recipe_id>/open_recipe/", views.open_recipe, name="open_recipe"),
    path("<int:recipe_id>/create_review/", views.create_review, name="create_review"),
    path("<int:review_id>/edit_review/", views.edit_review, name="edit_review"),
    path("<int:review_id>/delete_review/", views.delete_review, name="delete_review"),
    path("search/", views.search, name="search"),
    path("profile/", views.edit_profile, name="edit_profile"),
    path("register/", views.register, name="register"),
    path("chat/", views.chat_home, name="chat_home"),
    path("<str:user_username>/chat_room/", views.chat_room, name="chat_room"),
    path("<str:room_name>/delete_room/", views.delete_room, name="delete_room"),
]
