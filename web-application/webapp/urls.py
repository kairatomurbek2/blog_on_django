from django.conf.urls import url

from webapp import views
from accounts import views as accounts_view

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'categories/(?P<slug>[-_\w]+)/$', views.CategoriesView.as_view(), name='category_list'),
    url(r'categories/(?P<slug>[-_\w]+)/(?P<post_slug>[-_\w]+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^login/', accounts_view.LoginView.as_view(), name='login'),
    url(r'^logout/', accounts_view.LogoutView.as_view(), name='logout'),
    url(r'^registration/', accounts_view.RegistrationView.as_view(), name='registration'),
]
