from rest_framework import routers
from mysite import views as myapp_views
from django.urls import path,include

router = routers.DefaultRouter()


router.register(r'users', myapp_views.profileViewset)
router.register(r'child', myapp_views.childViewset)
router.register(r'attendence', myapp_views.attendenceViewset)
router.register(r'notification', myapp_views.NotificationViewset)
router.register(r'child_stories', myapp_views.child_storiesViewset)
router.register(r'leaves', myapp_views.LeavesViewset)


