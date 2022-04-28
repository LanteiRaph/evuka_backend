from django.shortcuts import render

# Create your views here.
from decimal import Decimal
import json
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Topic, Course
from .serializers import (
    CourseDisplaySerializer,
    CourseUnpaidserializer,
    CourseListSerializer,
    CoursePaidSerializer,
    CommentSerializer,
    CartItemSerializer
)# Create your views here.


class CourseHomeView(APIView):

    # returns courses based on topics and categorise
    def get(self, request, *args, **kwargs):
        # Get All categories availabe/topic
        topics = Topic.objects.all().order_by('?')[:6]

        output_responce = []

        for topic in topics:
            topic_courses = topic.related_cousres.order_by('?')[:4]
            courses_serializer = CourseDisplaySerializer(
                topic_courses, many=True)

            topic_output = {
                'topic_name': topic.name,
                'topic_code': topic.code,
                'featured_coureses': courses_serializer.data,
                'topic_image': topic.image.url
            }

            output_responce.append(topic_output)

        return Response(data=output_responce, status=status.HTTP_200_OK)


class CourseDetaiView(APIView):

    def get(self, request, code, *args, **kwargs):
        # Get the couse that match the cousrse code
        try:
            course = Course.objects.filter(code=code)
        except ValidationError:
            return HttpResponseBadRequest('Invalid Course uuid')
        if not course:
            return HttpResponseBadRequest("Course does not exist")
        # get all the sections that match the
        output = CourseUnpaidserializer(course[0])
        #Return the output data needed by the frontend
        return Response(data=output.data, status=status.HTTP_200_OK)


class CourseSearch(APIView):
    def get(self, request, topic_code, *args, **kwargs):
        #Get all the Topics and filter by topic id
        sector = Topic.objects.filter(code=topic_code)
        print(sector)
        #If non: Return bad request.
        if not sector:
            return HttpResponseBadRequest("Course Topic does not exist")
        #Get the only element in the record
        sector_courses = sector[0].related_cousres.all()
        #Serializ the data for the front end usage.
        serializer = CourseListSerializer(sector_courses, many=True)
        #Init the totals students value
        total_students = 0
        #Step thouth the corse and find the enerolled students.
        for course in sector_courses:
            total_students += course.get_enrolled_students()
        #Responde back to the user.
        return Response({'data': serializer.data,
                        'sector_name': sector[0].name,
                         'total_students': total_students,
                         'image': sector[0].image_url.url},
                        status=status.HTTP_200_OK)

class CourseStudy(APIView):
    #Get curerent logged in user.
    # permission_classes=[IsAuthenticated]


    def get(self,request,course_uuid):
        #Get the courses matching the given id.
        check_course=Course.objects.filter(code=course_uuid)
        #Non was found...
        if not check_course:
            #rreturn bad responce.
            return HttpResponseBadRequest('Course does not exist')
        #Course found Get the course for the current user
        user_course=request.user.paid_courses.filter(code=course_uuid)
        #If not founf
        if not user_course:
            return HttpResponseNotAllowed("User has not purchased this course")
        #course found Fethc the first one (onlyone)
        course=Course.objects.filter(code=course_uuid)[0]
        #Serilalze the data
        serializer=CoursePaidSerializer(course)
        #Respond back to the user...
        return Response(serializer.data,status=status.HTTP_200_OK)


class SearchCourse(APIView):

    def get(self,request,search_term):
        matches= Course.objects.filter(Q(title__icontains=search_term)|
            Q(description__icontains=search_term))

        serializer=CourseListSerializer(matches,many=True)

        return Response(data=serializer.data)



class AddComment(APIView):
    # permission_classes=[IsAuthenticated]

    #define the post method to handle incoming comments
    def post(self,request,course_code,*args, **kwargs):
        try:
            course=Course.objects.get(code=course_code)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        content=json.loads(request.body)
        if not content.get('message'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(data=content)

        if serializer.is_valid():
            comment=serializer.save(user=request.user)
            course.comment.add(comment)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class GetCartDetail(APIView):
    def post(self,request,*args, **kwargs):

        try:
            body =  json.loads(request.body)

        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest()

        if type(body.get('cart')) != list:
            return HttpResponseBadRequest()


        if len(body.get("cart")) ==0:
            return Response(data=[])

        courses=[]

        for uuid in body.get("cart"):
            item = Course.objects.filter(course_uuid=uuid)

            if not item:
                return HttpResponseBadRequest()

            courses.append(item[0])

            # serializer for cart
        serializer =CartItemSerializer(courses,many=True)

        # TODO : After you have added the price field
        cart_cost=Decimal(0.00)

        for item in serializer.data:

            cart_cost+=Decimal(item.get("price"))


        return Response(data={"cart_detail":serializer.data,"cart_total":str(cart_cost)})
