
from os import name, stat
from . import views
from django.urls import path
from function.settings import MEDIA_URL
from .views import PostListView,   PostDetailView , PostEditView, PostDeleteView, CommentDeleteView, Post_List_EditView, Post_List_DeleteView, Addlike, Dislike,PostNofication,RemoveNotification, CreateThread,ListThread,ThreadView,CreateMessage,ThreadNotification,ThreadDelete, SharedPostView, UserDeleteView, CommentDislike,CommentLike
#avatar image
from django.conf import settings
from django.conf.urls.static import static
app_name = 'main'
urlpatterns = [
    path('',views.home, name  = 'home'),
    path('login/',views.login_1, name = "login"),
    path('sign-up/',views.signup_1,name="sign-up"),
    path('login/home-login/',views.home_login,name = "home-login"),
    path('see-info/<str:pk>/',views.see_info, name = "see-info"),
    # path('create-form/',views.createform, name = "create-form"),
    path('logout/',views.logout_1,name = 'logout'),
    path('profile/<int:pk>/',views.profile, name = "profile"),
    # path('delete/<str:pk>/',views.delete,name = "delete"),
    path('search/',views.search, name = "searched"),
    path('searchpost/', views.search_post, name="search-post"),
    path('set-up-profile/',views.setup, name = "set-up"),
    path('set-up/',views.setup_profile, name = "set-up-profile"),
    path('about-us', views.about,  name= "about"),
    path('profile/<int:pk>/delete', UserDeleteView.as_view(), name= "user-delete"),

    #video chat
    path('lobby/',views.lobby, name= "lobby"),
    path("room/",views.room , name= "room"),
    #sharepost
    path('post/<int:pk>/share', SharedPostView.as_view(), name="share-post"),
    #post
    path('post/<int:pk>/', PostDetailView.as_view(),name="post-details"),
    path('post-list/',PostListView.as_view(), name='post-list'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name = 'post-edit'),

    path('post/delete/<int:pk>/',PostDeleteView.as_view(), name = "post-delete"),
    path('post/<int:post_pk>/comment/delete/<int:pk>/',CommentDeleteView.as_view(), name="comment-delete"),
    path('post-list/edit/<int:pk>/', Post_List_EditView.as_view(), name = 'postlist-edit'),
    path('post-list/delete/<int:pk>/',Post_List_DeleteView.as_view(), name = "postlist-delete"),
    #like and dislike
    path('post/<int:pk>/like', Addlike.as_view(), name="Like"),
    path('post/<int:pk>/dislike',Dislike.as_view(), name  ="Dislike"),
    #comments like and dislike  
    path('comment/<int:pk>/like', CommentLike.as_view(), name="comment-like"),
    path('comment/<int:pk>/dislike', CommentDislike.as_view(), name="comment-dislike"),
    #notifications
    path('notification/<int:notification_pk>/post/<int:post_pk>',PostNofication.as_view(), name="post-notification"),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name = "notification-delete"),
    path('notification/<int:notification_pk>/thread/<int:object_pk>/', ThreadNotification.as_view(), name = "thread-notification"),
    #CHAT
    path('inbox/',ListThread.as_view(), name = 'inbox'),
    path('inbox/create-thread/',CreateThread.as_view(), name = 'create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name = "thread"),
    path('inbox/<int:pk>/create-message/' , CreateMessage.as_view(), name= "create-message"),
    path('inbox/delete/<int:pk>/', ThreadDelete.as_view(), name="thread-delete"),
    #

    path('sayonara/', views.rate, name='sayonara'),
    #report 
    path('report/', views.report, name = "report"),


] 
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)