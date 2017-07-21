from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^quotes$', views.quotes),
	url(r'^new_quote', views.new_quote),
	url(r'^users/(?P<id>\d+)', views.user),
	url(r'^favorite/(?P<id>\d+)', views.favorite),
	url(r'^unfavorite/(?P<id>\d+)', views.unfavorite)
]