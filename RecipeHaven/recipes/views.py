from django.shortcuts import render
from .models import Recipe, Review, Room, Message
from .forms import RecipeForm, UserRegisterationForm, ReviewForm, EditProfileForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Avg

# Create your views here.


# These routes are for the Recipes
def recipe_list(request):
    category = request.GET.get("category")
    if category:
        recipes = Recipe.objects.filter(category=category).order_by("-created_at")
    else:
        recipes = Recipe.objects.all().order_by("-created_at")
    return render(request, "recipe/recipe_list.html", {"recipes": recipes})


@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect("recipe/recipe_list")
    else:
        form = RecipeForm()
    return render(request, "recipe/recipe_form.html", {"form": form})


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, user=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect("recipe/recipe_list")
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "recipe/recipe_form.html", {"form": form})


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, user=request.user)
    if request.method == "POST":
        recipe.delete()
        return redirect("recipe/recipe_list")
    return render(request, "recipe/recipe_confirm_delete.html", {"recipe": recipe})


@login_required
def open_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    review_list = Review.objects.filter(recipe=recipe)
    total_number_of_comments = review_list.count()
    average_rating = review_list.aggregate(Avg("rating"))["rating__avg"]
    if not average_rating:
        average_rating = 0

    return render(
        request,
        "recipe/recipe_detail.html",
        {
            "recipe": recipe,
            "total_number_of_comments": total_number_of_comments,
            "average_rating": average_rating,
        },
    )


@login_required
def create_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    review_list = Review.objects.filter(recipe=recipe)
    user_review_exists = review_list.filter(user=request.user).exists()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            return render(request, "recipe/recipe_detail.html", {"recipe": recipe})
    else:
        form = ReviewForm()
    return render(
        request,
        "reviews/review_form.html",
        {
            "recipe": recipe,
            "form": form,
            "review_list": review_list,
            "user_review_exists": user_review_exists,
        },
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("recipe/recipe_list")
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/review_form.html", {"form": form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect("recipe/recipe_list")
    return render(request, "reviews/review_delete_form.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("recipe/recipe_list")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, "user/edit_profile.html", {"form": form})


def search(request):
    query = request.GET.get("q")
    if query:
        recipes = Recipe.objects.filter(title__icontains=query)
    else:
        recipes = Recipe.objects.all()
    return render(request, "recipe/recipe_list.html", {"recipes": recipes})


# This route is for user registration
def register(request):
    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("recipe/recipe_list")
    else:
        form = UserRegisterationForm()
    return render(request, "registration/register.html", {"form": form})


# chat feature views


@login_required
def chat_home(request):
    users = User.objects.all()
    return render(request, "chat/chat_home.html", {"users": users})


@login_required
def chat_room(request, user_username):
    current_user_username = request.user.username
    other_user_username = user_username
    room_name = "_".join(sorted([current_user_username, other_user_username]))

    other_user = get_object_or_404(User, username=user_username)
    if other_user == request.user:
        return redirect("chat_home")

    try:
        get_room = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        new_room = Room(room_name=room_name)
        new_room.save()
        get_room = Room.objects.get(room_name=room_name)

    messages = Message.objects.filter(room=get_room)

    context = {
        "room_name": room_name,
        "other_user": other_user,
        "current_user": request.user,
        "messages": messages,
    }
    return render(request, "chat/chat_room.html", context)

@login_required
def delete_room(request, room_name):
    get_room = Room.objects.get(room_name=room_name)
    if request.method == "POST":
        get_room.delete()
        return redirect("chat_home")
    return render(request, "chat/chat_delete_form.html")
