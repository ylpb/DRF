from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^publish/$',views.PublishAPIView.as_view()),
    url(r'^publish/(?P<pk>\d+)$',views.BookAPIView.as_view()),
    url(r'^books/$',views.BookAPIView.as_view()),
    url(r'^books/(?P<pk>\d+)$',views.BookAPIView.as_view())
]
