from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('panel', views.PanelViewSet)

urlpatterns = [
    url(r'^panel/(?P<panelid>\d+)/analytics/$', views.HourAnalyticsView.as_view()),
    url(r'^panel/(?P<panelid>\d+)/analytics/day/$', views.DayAnalyticsView.as_view()),
]

urlpatterns += router.urls
