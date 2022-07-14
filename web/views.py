

from ast import Del
from cgi import print_form
from concurrent.futures import thread
from email.message import Message

from webbrowser import get
from xml.dom.expatbuilder import theDOMImplementation
from django.dispatch import receiver

from flask import request_started
from .forms import  ImageForm, MessageForm, NewUserForm, ThreadForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from .models import Gender, Notification, ThreadModel, User, Post,Comment, Profile,ThreadModel, MessageModel, Image
from django.http.response import JsonResponse
from .forms import UserCreationForm, PostForm, CommentForm, ThreadForm, MessageForm, ShareForm, ContactForm,ContactForm_Report, ImageForm
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404,redirect
import json
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import auth
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.
def report (request):
    if request.method == "POST":
        form = ContactForm_Report(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            content = form.cleaned_data['content']
            print("The form is valid")
            html = render_to_string('contactform.html',{
                'name':name,
                'email':email,
                'content':content,
            })
            send_mail('The Contact form subject',
            'This is  the message', 
            'celgamerx123@gmail.com',
            ['marcelaribal963@gmail.com'], html_message=html)
            return redirect('/login/home-login')
    else:
        
        form = ContactForm_Report()

    context = {
        'form':form
    }
    return render(request, 'report.html', context)
def rate(request):
    return render(request, 'rate.html')
def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            content = form.cleaned_data['content']
            print("The form is valid")
            html = render_to_string('contactform.html',{
                'name':name,
                'email':email,
                'content':content,
            })
            send_mail('The Contact form subject',
            'This is  the message', 
            'celgamerx123@gmail.com',
            ['marcelaribal963@gmail.com'], html_message=html)

            return redirect('main:sayonara')
    else:
        form = ContactForm()

    context = {
        'form':form
    }
    return render (request,'home.html', context)
def signup_1(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST ['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email exist, type another one')
                return redirect('/sign-up')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username exist, type another one')
                return redirect('/sign-up')
            else:
                user = User.objects.create_user(username=username ,email=email, password=password)
                user.save()
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password= password)
                auth.login(request, user_login)

                return redirect('/set-up-profile')
        else:
            messages.info(request,'Check Password if correct')
            return redirect ('/sign-up')
    # if request.method == "POST":
    #     form = NewUserForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
    #         username = form.cleaned_data.get('username')
    #         messages.success(request,f"{username}!!" )
    #         return HttpResponseRedirect ('/')
    #     messages.error(request, "Invalid Information! Try Again")
    # form = NewUserForm()
    return render (request=request, template_name='signup.html')
def login_1(request):

    if request.method =="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password= password)
            if user is not None:
                login(request,user)
                messages.success(request, f'Ohayo!')
                return redirect ('/login/home-login')
            else:
                messages.error(request, 'Invalid Username or password!')
        else:
            messages.error(request, 'Invalid Username or password! ')
    form = AuthenticationForm()
    return render(request = request, template_name= "login.html",context = {"login_form":form})
def thankyou(request):
    return render(request, 'thankyou.html')
def logout_1 (request):
    logout(request)
    messages.success(request,'Thankyou For Visiting!')
    return redirect('/')

@login_required(login_url= "/login" )
def home_login(request):


    user = User.objects.all().order_by('-created_on')
    context = {

        'user':user

    }
    return render(request,'home_login.html',context)

# @login_required(login_url= "/login" )
# def createform(request):
#     form = UserUpdateForm()
#     context = {"form":form}
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/login/home-login')
#     return render(request, 'createform.html',context)

@login_required(login_url= "/login" )
def profile(request, pk, *args,**kwargs):

    form = User.objects.get(id=pk)
    user = form.id
    user1 = Post.objects.filter(author=user).order_by('-created_on')

    if request.method == "POST":    
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f" Your Account has been updated ")
            return redirect ('/profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance= request.user.profile)
    context = {
        'u_form':u_form,
        'p_form':p_form,
        'user1':user1,

    }

    return render(request, 'profile.html',context)


# @login_required(login_url= "/login" )
# def delete(request, pk):
#     forms = Information.objects.get(id = pk)
#     if request.method == "POST":
#         forms.delete()
#         return redirect('/login/home-login')
#     return render (request, 'delete.html', context = {"forms":forms})
@login_required(login_url= "/login" )
def see_info(request, pk, *args, **kwargs):
    form = User.objects.get(id=pk)
    user = form.id
    user1 = Post.objects.filter(author=user).order_by('-created_on')
   

    context = {"form":form, 'user1':user1 }
    return render (request, 'Seemoreinfo.html',context)
@login_required(login_url= "/login" )

def search(request):     
        if request.method == "GET":
            searched = request.GET.get('searched')
            post = User.objects.all().filter(name__icontains=searched)
            return render (request, 'search.html', {"post":post})
@login_required(login_url="/login")
def search_post(request):
    if request.method == "GET":
        searched = request.GET.get('search_post')
        search = Post.objects.all().filter(post__icontains=searched)
        return render(request, 'search_post.html',{'search':search})
@login_required(login_url= "/login" )
def setup(request):
    user = request.user
    form = UserUpdateForm(instance=user)

    if request.method == "POST":    
        form = UserUpdateForm( request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f" Welcome {username}!!")
            return redirect ('/', pk=user.id)
    context = {
        'form':form,
    }
    return render(request, 'profile_setup.html',context)

@login_required(login_url= "/login" )
def setup_profile(request):
    user = request.user
    form = UserUpdateForm(instance=user)

    if request.method == "POST":    
        form = UserUpdateForm( request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            messages.success(request, f" Your Account has been updated ")
            return redirect ('main:profile', pk=user.id)
    context = {
        'form':form,
    }
    return render(request, 'setup.html',context)


#video chat
def lobby (request):
    return render(request, 'lobby.html')

def room(request):
    return render(request, 'room.html')



# sharepost
class SharedPostView(View):
    def post (self,request,pk ,*args,**kwargs):
        original_post = Post.objects.get(pk=pk)
        form = ShareForm(request.POST)

        if form.is_valid():
            new_post = Post(
                shared_body =self.request.POST.get('body'),
                post= original_post.post,
                author = original_post.author,
                created_on = original_post.created_on,
                shared_user = request.user,
                shared_on = timezone.now(),
            )
            new_post.save()

            for img in original_post.image.all():
                new_post.image.add(img)
            new_post.save()
        return redirect('main:post-list')

# post 
class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        form = PostForm()
        share_form = ShareForm()

   
        context= {
            'post_list':posts,
            'form':form,
            'shareform':share_form


         
        }   
        return render(request, 'postlist.html', context)
    def post(self,request,*args, **kwargs):
        try:
            posts = Post.objects.all()
        except Post.DoesNotExist:
            posts = None
        #request.files is for image adding in website
       
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        share_form = ShareForm()

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()  

        context= {
            
            'post_list':posts,
            'form':form,
            'shareform': share_form,
      

        }   

        return render(request, 'postlist.html', context)
def about(request):
    return render(request, 'about_us.html')
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk,*args, **kwargs):
        post = Post.objects.get(pk=pk)
        share_form = ShareForm()
        form = CommentForm()
      
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        context = {
            'post':post,
            'form':form,
            'comments':comments,
            'share_form':share_form,


        }
        return render(request,'postdetail.html', context)
    def post(self,request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        share_form = ShareForm()

        if form.is_valid():
            new_comment =form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        notification = Notification.objects.create(notification_type=2,from_user=request.user, to_user=post.author,post=post)
        context = {
            'post':post,
            'form':form,
            'comments':comments,
            'share_form':share_form,



        }
        return render(request,'postdetail.html', context)
class PostEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post

    fields = ['post']

    template_name = 'post_edit.html'
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('main:post-details', kwargs={'pk':pk})
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url= reverse_lazy('main:post-list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class UserDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = User
    template_name = "user_delete.html"
    success_url = reverse_lazy ('main:home')
    def test_func(self):
        user = self.get_object()
        return self.request.user == user
class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comment
    template_name = "comment_confirm_delete.html"
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('main:post-details', kwargs={'pk':pk})
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
class Post_List_EditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['post','image']
    template_name = 'post_list_edit.html'
    def get_success_url(self):
        return reverse_lazy('main:post-list',)
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
class Post_List_DeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'post-list_delete.html'
    success_url= reverse_lazy('main:post-list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
class CommentLike(LoginRequiredMixin,View):
    def post(self, request, pk ,*args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            comment.dislikes.remove(request.user)
        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1,from_user=request.user, to_user=comment.author,comment=comment)
        if is_like:
            comment.likes.remove(request.user)
        next= request.POST.get('next','/post-details')
        return HttpResponseRedirect(next)
class Addlike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
          
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1,from_user=request.user, to_user=post.author,post=post)
        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next','/post-list')
        return HttpResponseRedirect(next)
class CommentDislike(LoginRequiredMixin,View):
    def post (self,request,pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            comment.likes.remove(request.user)
        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if not is_dislike:
            comment.dislikes.add(request.user)
            notification = Notification.objects.create(notification_type=1,from_user=request.user, to_user=comment.author,comment=comment)
        if is_dislike:
            comment.dislikes.remove(request.user)
        next= request.POST.get('next','/post-details')
        return HttpResponseRedirect(next)
class Dislike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            post.likes.remove(request.user)
        
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if not is_dislike:
            post.dislikes.add(request.user)
        if is_dislike:
            post.dislikes.remove(request.user)
        
        next = request.POST.get('next','/post-list')
        return HttpResponseRedirect(next)

class PostNofication(View):
    def get(self, request, notification_pk, post_pk, *args , **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('main:post-details',pk=post_pk)

class RemoveNotification(View):
    def delete(self,request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success',content_type = "text/plain")
#message chat
#------------------------------------------------------------------------------------------------
#notification thread
class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk , *args , **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save() 
        return redirect('main:thread', pk = object_pk)
class ThreadDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = ThreadModel
    template_name = 'thread_delete.html'
    success_url= reverse_lazy('main:inbox')
    
    def test_func(self):
        thread = self.get_object()

        return self.request.user == thread.user , self.request.user == thread.receiver
class ListThread(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'inbox.html', context)
class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        

        context = {
            'form': form
        }

        return render(request, 'create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('main:thread', pk=thread.pk)
        except:
            messages.error(request,'Invalid Username')
            return redirect('main:create-thread')
class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list,
        }

        return render(request, 'thread.html', context)
class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form =  MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message= form.save(commit=False)
            message.thread = thread
            message.sender = request.user
            message.receiver_user = receiver
            message.save()

        message = MessageModel(
            thread=thread,
            sender=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )


        # notification
        notification = Notification.objects.create(notification_type=4, 
        from_user = request.user,
        to_user = receiver,
        thread = thread,
        )
        return redirect('main:thread', pk=pk)
