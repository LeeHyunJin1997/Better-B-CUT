from django.urls import path
from . import views

app_name = 'opinion'

urlpatterns = [
    # opinion
    path('', views.opinion_list, name='opinion_list'),
    path('<int:opinion_id>', views.opinion_detail, name='opinion_detail'),
    path('<int:opinion_id>/like', views.like, name='like'),
    path('<int:opinion_id>/dislike', views.dislike, name='dislike'),
    # comment
    path('<int:opinion_id>/comment', views.comment_list, name='comment_list'),
    path('<int:opinion_id>/comment/<int:opinion_comment_id>', views.comment_detail, name='comment_datail'),
    path('<int:opinion_id>/comment/<int:opinion_comment_id>/like', views.comment_like, name='comment_like'),
]
