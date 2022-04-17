from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from tweets.models import Status
from .forms import SettingsForm, CommentForm
from accounts.models import CustomUser
from django.views import View
from django.views.generic.edit import (
    CreateView
)
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

@login_required
def feed(request):
    users_to_follow = []
    all_users = CustomUser.objects.all()

    feed = list(Status.objects.all().filter(creator=request.user))

    for user in request.user.following.all():
        for status in Status.objects.all().filter(creator=user):
            feed.append(status)

    for user in all_users:
        if user != request.user:
            users_to_follow.append(user)

    return render(request, 'pages/feed.html', {
        'users_to_follow': users_to_follow,
        'feed': feed
    })

@login_required
def explore(request):
    users_to_follow = []
    all_users = CustomUser.objects.all()
    for user in all_users:
        if user != request.user:
            users_to_follow.append(user)

    return render(request, 'pages/explore.html', {
        'users_to_follow': users_to_follow,
        'status_list': Status.objects.all()
    })

@login_required
# @user_passes_test(lambda user: user == )
def profile(request, username):
    users_to_follow = []
    all_users = CustomUser.objects.all()
    user_profile = CustomUser.objects.get(username=username)
    is_authorized = request.user == user_profile

    for user in all_users:
        if user != request.user:
            users_to_follow.append(user)

    context = {
        'user_profile': user_profile,
        'users_to_follow': users_to_follow,
        'is_authorized': is_authorized
    }

    return render(request, 'pages/profile.html', context)

@login_required
def likes(request, username, id):
    liked_post = get_object_or_404(Status, id=int(request.POST.get('status_id')))
    liked_post.likes.add(request.user)

    return HttpResponseRedirect(reverse('single_status', args=[liked_post.creator.username, liked_post.pk]))

@login_required
def follow(request, username1, username2):
    followed_user = get_object_or_404(CustomUser, username=request.POST.get('user_name'))
    followed_user.followers.add(request.user)

    return HttpResponseRedirect(reverse('profile', args=[followed_user.username,]))

class SingleStatusView(LoginRequiredMixin, View):
    def get(self, request, username, id):
        status = Status.objects.all().get(id=id)

        comment_form = CommentForm

        context = {
            'status': status,
            'comment_form': comment_form
        }

        return render(request, 'pages/single_status.html', context)

    def post(self, request, username, id):
        status = Status.objects.all().get(id=id)

        comment_form = CommentForm(request.POST, request.FILES)

        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.reply_on = status
            comment.save()

            return HttpResponseRedirect(reverse('single_status', args=[username, id,]))

        context = {
            'comment_form': comment_form,
        }

        return render(request, 'pages/single_status.html', context)

class NewStatusView(LoginRequiredMixin, CreateView):
    template_name = 'pages/new_status.html'
    model = Status
    fields = ('status_text', 'image',)
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class SettingsView(LoginRequiredMixin, View):
    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        all_users = CustomUser.objects.all()
        users_to_follow = []

        update_form = SettingsForm(initial={'username': username, 'email': user.email})

        for user in all_users:
            if user != request.user:
                users_to_follow.append(user)

        context = {
            'update_form': update_form,
            'users_to_follow': users_to_follow
        }

        return render(request, 'pages/settings.html', context)

    def post(self, request, username):
        update_form = SettingsForm(request.POST, request.FILES)
        
        if update_form.is_valid():
            changed = update_form.cleaned_data
            user = CustomUser.objects.get(username=username)

            user.username = changed['username']
            user.email = changed['email']
            user.image = changed['image']

            user.save()

            return HttpResponseRedirect(reverse('profile', args=[user.username,])) 

        context = {
            'update_form': update_form,
        }

        del_user = request.POST.get('del_user')
        if del_user != None and del_user != '':
            CustomUser.objects.get(username=del_user).remove()
        
        return render(request, 'pages/settings.html', context)
        