from django.conf.urls import url
from django.urls import path , include
from . import views
#REST API URLS


from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
 
    url(r'^$', views.home, name="home"),
    url(r'login/', views.login_user, name = 'login'),
    url(r'^logout/$', views.logout_user, name= "logout"),
    url(r'^register/$', views.register_user, name= "register"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'edit-profile/$', views.edit_profile, name="editProfile"),
    url(r'edit-profile-inform/$', views.edit_profile_user, name="editProfileUSer"),

    #Password Change URL............
    url(r'^change_password/$', views.change_password, name = "change_password"),

    #password Reset URLS...........
    path('password_reset/', PasswordResetView.as_view(), name='password_reset' ),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact/$', views.contact, name= "contact"),

    #RESTAPI  ...................
    path('rest-auth/', include('rest_auth.urls')),
    #path('rest-auth/register/', include('rest_auth.registration.urls')),
    path('users/', views.ListprofileView.as_view(), name="users"),
    path('attendence/', views.attendenceView.as_view(), name="attendence"),
    path('notification/', views.NotificationView.as_view(), name="notification"),
    path('child_stories/', views.child_storiesView.as_view(), name="child_stories"),
    path('leaves/', views.LeavesView.as_view(), name="leaves"),
    path('users/<int:pk>/', views.profileDetail.as_view()),
    path('attendence/<int:pk>/', views.attendenceDetail.as_view()),
    path('notification/<int:pk>/', views.NotificationDetail.as_view()),
    path('child_stories/<int:pk>/', views.child_storiesDetail.as_view()),
    path('leaves/<int:pk>/', views.LeavesDetail.as_view()),
    

    


    #Parents ....................
    #child
    path('childform/$',views.childview,name='childform'),
    url(r'^childlist/(?P<user>[-\w]+)/$',views.childlist,name='childlist'),
    #attendence
    url(r'^attendencelist/(?P<user>[-\w]+)/$',views.attendencelist,name='attendencelist'),
    url(r'^pick/(?P<user>[-\w]+)/$', views.picklist, name="pick"),
    url(r'^attenndenceformedit/(?P<id>\d+)/$', views.attendenceformedit, name="attenndenceformedit"),
    url(r'^attenndenceform/(?P<id>\d+)/$', views.attenndenceview, name="attenndenceform"),
    url(r'^attendencelistteacher/$',views.attendencelistteacher,name='attendencelistteacher'),
    url(r'^notificationview/$',views.notificationview,name='notificationview'),
    url(r'^notifcationlist/$',views.notifcationlist,name='notifcationlist'),
    url(r'^notificationedit/(?P<id>\d+)/$', views.notificationedit, name="notificationedit"),
    url(r'^child_storiesview/(?P<id>\d+)/$', views.child_storiesview, name="child_storiesview"),
    url(r'^childstorylist/$', views.childstorylist, name="childstorylist"),
    url(r'^childstorieslistparent/(?P<user>[-\w]+)/$', views.childstorieslistparent, name="childstorieslistparent"),
    url(r'^childstoriesviewparent/(?P<id>\d+)/$', views.childstoriesviewparent, name="childstoriesviewparent"),
    url(r'^notifcationlistparent/$',views.notifcationlistparent,name='notifcationlistparent'),
    url(r'^childviewedit/(?P<id>\d+)/$', views.childviewedit, name="childviewedit"),
    url(r'^childlistprofile/(?P<user>[-\w]+)/$', views.childlistprofile, name="childlistprofile"),
    url(r'^childlistprofileteacher/$',views.childlistprofileteacher,name='childlistprofileteacher'),
    url(r'^leavesview/$',views.leavesview,name='leavesview'),
    url(r'^leaveslist/(?P<user>[-\w]+)/$',views.leaveslist,name='leaveslist'),
    url(r'^leaveslistteacher/$',views.leaveslistteacher,name='leaveslistteacher'),
    url(r'^leavesviewedit/(?P<id>\d+)/$', views.leavesviewedit, name="leavesviewedit"),
    url(r'^games/$',views.games,name='games'),
    url(r'^game1/$',views.game1,name='game1'),
    url(r'^game2/$',views.game2,name='game2'),



  
  

  
]