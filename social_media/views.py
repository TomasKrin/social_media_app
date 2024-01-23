from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views import generic

from social_media.forms import UserPostForm
from social_media.models import UserPost


@csrf_protect
def register_user(request):
    if request.method != "POST":
        return render(request, 'registration/registration.html')

    username = request.POST["username"]
    email = request.POST["email"]
    first_name = request.POST["name"]
    last_name = request.POST["lastname"]
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

    User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                             last_name=last_name)
    messages.success(request, "User %s registered!!!" % username)
    return redirect('login')


def socialmedia_index(request):
    if request.user.is_authenticated:
        return redirect('posts')
    else:
        return render(request, 'socialmedia-index.html')


class UserPostsView(generic.edit.FormMixin, generic.ListView):
    model = UserPost
    context_object_name = 'post_list'
    template_name = 'post_list.html'
    form_class = UserPostForm
    success_url = reverse_lazy('posts')

    def get_queryset(self):
        # Order by 'date_posted' in descending order (newest first)
        return UserPost.objects.all().order_by('-date_posted')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # formos custom validacija
    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)

# class CreatePost(generic.CreateView):
#     model = UserPost
#     form_class = UserPostForm
#     success_url = 'socialmedia/posts'
#     template_name = 'post-list.html'

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
