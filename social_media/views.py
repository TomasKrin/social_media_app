from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def register_user(request):
    if request.method != "POST":
        return render(request, 'registration/registration.html')

    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    password2 = request.POST["password2"]

    if password != password2:
        messages.error(request, "Passwords don't match!!!")

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username %s already exists!!!" % username)

    if User.objects.filter(email=email).exists():
        messages.error(request, f"Email {email} already exists!!!")

    if messages.get_messages(request):
        return redirect('register-url')

    User.objects.create_user(username=username, email=email, password=password)
    messages.success(request, "User %s registered!!!" % username)
    return redirect('login')


def socialmedia_index(request):
    return render(request, 'socialmedia-index.html')

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f"Profilis sėkmingai atnaujintas!!!")
#             return redirect('profile-url')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }
#     return render(request, 'profile.html', context=context)
