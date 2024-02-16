
from django.urls import path
from .views import *

urlpatterns = [

    path("",home),
        path('query/', query_view, name='query'),
        path('get-chat/', get_conversation, name='Get_Conversation'),
    path('get-session-id/', get_session_id, name='get_session_id'),

]

