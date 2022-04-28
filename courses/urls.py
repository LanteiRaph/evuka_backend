from django.urls import path, include
from courses import views


app_name='courses'
urlpatterns = [
    path('', views.CourseHomeView.as_view(), name='Home'),
    path('details/<uuid:code>/', views.CourseDetaiView.as_view(), name='course-detail'),
    path("study/<uuid:course_uuid>/",views.CourseStudy.as_view()),#405 Error(reasearch)
    path("search/<str:search_term>/",views.SearchCourse.as_view()),
    path('<uuid:topic_code>/',views.CourseSearch.as_view()),
    path('comment/<uuid:course_code>/',views.AddComment.as_view()),#Undebbuged
    path('cart/',views.GetCartDetail.as_view()),#Undebbuged
]


