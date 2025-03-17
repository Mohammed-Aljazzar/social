from django.shortcuts import get_object_or_404, render, redirect
from .forms import DweetForm
from .models import Profile , Dweet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard(request):
    form = DweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")
    if request.user.is_authenticated:
        followed_dweets = Dweet.objects.filter(
            user__profile__in=request.user.profile.follows.all()
        ).order_by("-created_at")
    else:
        followed_dweets = None

    return render(
        request,
        "dwitter/dashboard.html",
        {"form": form, "dweets": followed_dweets},
    )

    # form = DweetForm()
    # return render(request, "dwitter/dashboard.html", {"form": form})

@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

@login_required
def profile(request, pk):
    # Use get_object_or_404 to handle missing profiles
    profile = get_object_or_404(Profile, pk=pk)

    # Ensure the current user has a profile
    if request.user.is_authenticated and not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    if request.method == "POST" and request.user.is_authenticated:
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    return render(request, "dwitter/profile.html", {"profile": profile})


def all_users(request):
    # Get all users except the current user
    users = User.objects.exclude(id=request.user.id) if request.user.is_authenticated else User.objects.all()

    if request.method == "POST" and request.user.is_authenticated:
        # Handle follow action
        user_to_follow_id = request.POST.get("follow")
        if user_to_follow_id:
            user_to_follow = User.objects.get(id=user_to_follow_id)
            request.user.profile.follows.add(user_to_follow.profile)
            return redirect("dwitter:all_users")

    return render(request, "dwitter/all_users.html", {"users": users})