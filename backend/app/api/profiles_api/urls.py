from django.urls import path

from api.profiles_api.views import CreateUserView, ProfileRetrieveUpdateDestroy, CustomAuthToken

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create-user'),
    path('details/', ProfileRetrieveUpdateDestroy.as_view(), name='retrieve-update-delete-api-view'),
    path('login/', CustomAuthToken.as_view()),
]
