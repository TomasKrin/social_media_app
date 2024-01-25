from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views import generic

from social_media.forms import UserPostForm, UserUpdateForm, ProfileUpdateForm, CommentModelForm
from social_media.models import UserPost, Profile, PostLike


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

    comment_form_class = CommentModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.comment_form_class(prefix='comment')
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        comment_form = self.comment_form_class(request.POST, prefix='comment')
        if 'submit_post' in request.POST and form.is_valid():
            return self.form_valid(form)
        elif 'submit_comment' in request.POST and comment_form.is_valid():
            return self.comment_form_valid(comment_form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)

    def comment_form_valid(self, form):
        post_id = self.request.POST.get('post_id')
        post = get_object_or_404(UserPost, id=post_id)
        comment = form.save(commit=False)
        comment.profile = self.request.user.profile
        comment.post = post
        comment.save()
        messages.success(self.request, "Your comment has been added!")
        return redirect('posts')

    def get_queryset(self):
        return UserPost.objects.all().order_by('-date_posted')


@login_required
def my_profile_view(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile upadated!")
            return redirect('myprofile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    profile = Profile.objects.get(user=request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile,
        'friends_preview': profile.get_friends()[0:5]
    }

    return render(request, 'myprofile.html', context=context)


def profile_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    context = {
        'profile': profile,
        'friends_preview': profile.get_friends()[0:5]
    }
    if profile.user == request.user:
        return redirect('myprofile')

    profile.profile_views += 1
    profile.save()
    return render(request, 'profile_detail.html', context=context)


def friends_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    context = {
        'profile': profile,
        'friends': profile.get_friends()
    }

    return render(request, 'friendlist.html', context=context)


def like_unlike_post(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = UserPost.objects.get(id=post_id)
        profile = Profile.objects.get(user=request.user)
        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)

        like, like_added = PostLike.objects.get_or_create(profile=request.user.profile, post=post)

        if not like_added:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

        post.save()
        like.save()
        return redirect('posts')
