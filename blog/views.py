from django.shortcuts import render

# Create your views here.

from rest_framework import generics, views
from rest_framework.response import Response
from . import serializers
from .models import User, Post
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.decorators import login_required


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

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            context['author'] = User.objects.get(pk=self.kwargs["pk"])
        return context

class UserTable(ListView):
    model = User
    template_name = "user_list.html"


class DeletePost(DeleteView):
    model = Post
    template_name='confirm_delete-a.html'
    success_url = "."


class AddPost(CreateView):
    model = Post
    fields = ["title", "body"]
    template_name = "post_add.html"
    success_url = "."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()


class PostList(generics.ListCreateAPIView):
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Post.objects.filter(user_id=self.kwargs["pk"])
        else:
            return Post.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()


class PostDetail(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, serializer):
        instance = serializer.delete()
