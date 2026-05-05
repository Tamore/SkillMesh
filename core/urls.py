from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/add-skill/', views.add_skill, name='add_skill'),
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:post_id>/edit/', views.edit_post_view, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('message/send/<str:username>/', views.send_message_view, name='send_message'),
    path('search/', views.search_view, name='search'),
    path('opportunities/', views.opportunities_view, name='opportunities'),
    path('insights/', views.insights_view, name='insights'),
    path('insights/export/', views.export_events_csv, name='export_events'),
    path('secret-sync-protocol/', views.seed_database_view, name='seed_database'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/save/', views.toggle_save, name='toggle_save'),
]
