from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^user/(?P<id>[0-9]+)/$', views.show_user, name='user show'),
    url(r'^question/(?P<id>[0-9]+)/$', views.show_question, name='question show'),
    url(r'^ask_question/$', views.show_ask_question, name='ask question'),
    url(r'^post_question/$', views.post_question, name='post question'),
    url(r'^add_recommendation/$', views.add_recommendation, name='add recommendation'),
    url(r'^upvote_question/$', views.upvote_question, name='upvote question'),
    url(r'^downvote_question/$', views.downvote_question, name='downvote question'),
    url(r'^upvote_recommendation/$', views.upvote_recommendation, name='upvote recommendation'),
    url(r'^downvote_recommendation/$', views.downvote_recommendation, name='downvote recommendation'),
    url(r'^spam_question/$', views.spam_question, name='spam question'),
    url(r'^spam_recommendation/$', views.spam_recommendation, name='spam recommendation'),


    # analysis
    url(r'^export_questions/$', views.export_questions, name='export question'),
]