from django.conf.urls import url
from FintechExplorerApp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^select_category$', views.select_category, name='select_category'),
    url(r'^taxonomy$', views.taxonomy, name='taxonomy'),
    url(r'^file_grid$', views.file_grid, name='file_grid'),
    url(r'^category_selected$', views.category_selected, name='category_selected'),
    url(r'^custom_search$', views.custom_search, name='custom_search')
]