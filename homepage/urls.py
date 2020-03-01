from django.conf.urls import url
#from .views import detect_emotion
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


app_name = 'homepage'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'homepage:index'}, name='logout'),
    url(r'^emotion/$', views.mood, name='emotion'),
    url(r'^detect_emotion$', views.detect_emotion, name='detect_emotion'),

    url(r'^summarize/$', views.summarize, name='summarize'),
    url(r'^display_summary$', views.display_summary, name='display_summary'),

    url(r'^categories/(?P<pk>\d+)/$', views.category_topics, name='category_topics'),
    url(r'^categories/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),

    url(r'^categories/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),

    url(r'^categories/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/post/$', views.new_post, name='new_post'),




]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
