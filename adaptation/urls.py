from django.urls import path
from . import views

app_name = 'adaptation'

urlpatterns = [
    # adaptation
    path('', views.adaptation_list, name='adaptation_list'),
    path('<int:adaptation_id>', views.adaptation_detail, name='adaptation_detail'),
    path('<int:adaptation_id>/like', views.like, name='like'),
    # comment
    path('<int:adaptation_id>/comment', views.comment_list, name='comment_list'),
    path('<int:adaptation_id>/comment/<int:adaptation_comment_id>', views.comment_detail, name='comment_datail'),
    path('<int:adaptation_id>/comment/<int:adaptation_comment_id>/like', views.comment_like, name='comment_like'),
]
