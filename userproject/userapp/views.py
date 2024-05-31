from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Stage, UserStageProgress
from .forms import UserRegistrationForm,UserProfileForm

# def timeline2_view(request):
#     stages = Stage.objects.all().order_by('order')
#     user_progress = UserStageProgress.objects.filter(user=request.user)
#     completed_stages = {progress.stage.id for progress in user_progress if progress.completed}

#     context = {
#         'stages': stages,
#         'completed_stages': completed_stages,
#     }
#     return render(request, 'timeline2.html',context)

@login_required
def timeline_view(request):
    stages = Stage.objects.all().order_by('order')
    user_progress = UserStageProgress.objects.filter(user=request.user)
    completed_stages = {progress.stage.id for progress in user_progress if progress.completed}

    context = {
        'stages': stages,
        'completed_stages': completed_stages,
    }
    return render(request, 'timeline.html', context)

@login_required
def complete_stage(request, stage_id):
    stage = Stage.objects.get(id=stage_id)
    progress, created = UserStageProgress.objects.get_or_create(user=request.user, stage=stage)
    progress.completed = True
    progress.save()
    return redirect('timeline')

@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user': request.user,
        'profile': user_profile,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            #UserProfile.objects.create(user=new_user)  # Create a UserProfile instance
            # Authenticate and login the user
            user = authenticate(username=new_user.username, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
