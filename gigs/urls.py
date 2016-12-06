from django.conf.urls import url
from . import views

app_name = 'gigs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_gig/$', views.add_edit_gig, name='add_gig'),
    url(r'^(?P<gig_id>\d+)/edit/$', views.add_edit_gig, name='edit_gig'),
    url(r'^delete/(?P<pk>\d+)/$', views.GigDelete.as_view(), 
                                  name='delete_gig'),
    url(r'^summary/$', views.summary, name='summary'),
]