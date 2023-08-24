from django.urls import path
from .views import *

urlpatterns = [
    path('', BulletinsList.as_view()),
    path('<int:pk>', BulletinDetail.as_view(), name='bulletin'),
    path('create', BulletinCreate.as_view(), name='create'),
    path('search', BulletinsSearch.as_view(), name='search'),
    path('<int:pk>/edit', BulletinEdit.as_view(), name='edit'),
    path('<int:pk>/delete', BulletinDelete.as_view(), name='delete'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/profilelist', ProfileList.as_view(), name='profilelist'),
    path('profile/replies', ReplyList.as_view(), name='replies'),
    path('profile/replies/<int:pk>/reply_accept', reply_accept, name='reply_accept'),
    path('profile/replies/<int:pk>/reply_disaccept', reply_disaccept, name='reply_disaccept'),
    path('profile/self_replies', SelfReplyList.as_view(), name='self_replies'),
    path('profile/replies/<int:pk>/editrep', ReplyEdit.as_view(), name='editrep'),
    path('profile/replies/<int:pk>/deleterep', ReplyDelete.as_view(), name='deleterep'),
    path('news', NewsView.as_view(), name='news'),
    path('news/news_subscribe', news_subscribe, name='news_subscribe'),
    path('news/news_unsubscribe', news_unsubscribe, name='news_unsubscribe'),
    path('news/<int:pk>', NewsDetail.as_view(), name='new'),
    path('news/createnews', NewsCreate.as_view(), name='createnews'),
    path('news/<int:pk>/editnews', NewsEdit.as_view(), name='editnews'),
    path('news/<int:pk>/deletenews', NewsDelete.as_view(), name='deletenews'),
]
