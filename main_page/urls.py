from django.urls import path
from . import views
urlpatterns = [
    path('api/v1/main/', views.MainPage.as_view()),
    path('api/v1/main/search/', views.MainPageSearch.as_view()),
    path('api/v1/main/salon/<int:id>/', views.BusinessAccountDetail.as_view()),
    path('api/v1/main/staff/<int:id>/', views.BusinessAccountStaff.as_view()),
    path('api/v1/main/staff/review/<int:id>/', views.StaffReview.as_view()),
    path('api/v1/main/salon/review/<int:id>/', views.SalonReview.as_view()),
    path('api/v1/main/service/<int:id>/', views.BusinessAccountService.as_view()),
    path('api/v1/main/salon/<int:id>/', views.BusinessAccountDetail.as_view()),
    path('api/v1/records/', views.CreateListRecordsAPIView.as_view()),
    path('api/v1/timelist/<int:id>/', views.ListTimeRecordsAPIView.as_view()),
    path('api/v1/daylist/<int:id>/', views.ListFreeDayAPIView.as_view()),
    path('api/v1/records/user/<int:id>/', views.ListUserRecordsAPIView.as_view())
]
