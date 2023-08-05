from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from . import serializers
from .models import User, Post
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView

# Ui part ###
mainmenu = TemplateView.as_view(template_name='mainmenu.html')


class Blog(ListView):
    model = Post
    template_name = "Post_list.html"
    ordering = ['-created']

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Post.objects.filter(user_id=self.kwargs["pk"])
        else:
            return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            context['author'] = User.objects.get(pk=self.kwargs["pk"])
        return context


class UserTable(ListView):
    model = User
    template_name = "user_list.html"


class DeletePost(DeleteView):
    model = Post
    template_name = 'confirm_delete-a.html'
    success_url = "."


class AddPost(CreateView):
    model = Post
    fields = ["title", "body"]
    template_name = "post_add.html"
    success_url = "."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# API part ###


class UserList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()


class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Post.objects.filter(user_id=self.kwargs["pk"])
        else:
            return Post.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()


class PostDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.auth.user:
            raise PermissionDenied("can delete own only")
        instance = serializer.delete()
