from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from courses.models import Course,Comment,Section, Episode
from users.serializers import UserSerializer

class EpisodePaidSerializer(ModelSerializer):
    length=serializers.CharField(source='get_video_length_time')
    file=serializers.CharField(source='get_absolute_url')
    class Meta:
        model=Episode
        fields=[
            "title",
            "file",
            "length",
        ]

class CourseSectionPaidSerializer(ModelSerializer):
    episodes=EpisodePaidSerializer(many=True)
    # total_length=serializers.CharField(source='total_length')
    class Meta:
        model=Section
        fields=[
            "title",
            "episodes",
            "total_length"
        ]
class CourseDisplaySerializer(ModelSerializer):
    author = UserSerializer()
    image_url = serializers.CharField(source='get_absolute_url')
    class Meta:
        model = Course
        fields =[
            'code',
            'title',
            'price',
            'image_url',
            'author',
        ]

class CommentSerializer(ModelSerializer):
    user= UserSerializer(read_only=True)
    class Meta:
        model = Comment
        exclude= [
            'comment'
        ]
class UnpaidEpisodeSerializere(ModelSerializer):

    length = serializers.CharField(source= 'get_video_length_time')
    class Meta:
        model = Episode
        exclude = [
            'file'
        ]
class Sectionserializer(ModelSerializer):
    episodes = UnpaidEpisodeSerializere(many=True)
    total_episodes = serializers.ImageField(source='get_total_episodes')
    total_length = serializers.CharField(source='get_total_length')

    class Meta:
        model = Section
        fields = [
            'title',
            'episodes',
            'total_length',
            'total_episodes'
        ]
class CommentSerializer(ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Comment
        fields=[
            'user',
            'message',
            'created',
            'id'
        ]
class CourseUnpaidserializer(ModelSerializer):
    comment = CommentSerializer(many=True)
    sections = Sectionserializer(many=True)
    author = UserSerializer()
    enrolled_students = serializers.IntegerField(source='get_enrolled_students')
    total_episodes = serializers.IntegerField(source='get_total_lectures')
    total_length = serializers.CharField(source='get_total_length')
    class Meta:
        model=Course
        fields =[
            'title',
            'price',
            'description',
            'comment',
            'sections',
            'author',
            'enrolled_students',
            'total_length',
            'total_episodes'
        ]
class CoursePaidSerializer(ModelSerializer):

    comment=CommentSerializer(many=True)
    author=UserSerializer()
    sections=CourseSectionPaidSerializer(many=True)
    # student_rating=serializers.IntegerField(source='get_rating')
    # student_rating_no=serializers.IntegerField(source='get_no_rating')
    enrolled_students=serializers.IntegerField(source='get_enrolled_students')
    total_lectures=serializers.IntegerField(source="get_total_lectures")
    # total_length=serializers.CharField(source='get_total_length')
    class Meta:
        model=Course
        exclude=[
            'course',
        ]
class CourseListSerializer(ModelSerializer):
    # rating=serializers.IntegerField(source='get_rating')
    enrolled_students=serializers.IntegerField(source='get_enrolled_students')
    author=UserSerializer()
    description=serializers.CharField(source='get_brief_description')
    total_lectures=serializers.IntegerField(source="get_total_lectures")
    class Meta:
        model=Course
        fields=[
            'code',
            "title",
            'enrolled_students',
            "author",
            "price",
            "image_url",
            'description',
            'total_lectures']


class CartItemSerializer(ModelSerializer):
    author=UserSerializer()
    class Meta:
        model=Course
        # add price later,image url
        fields=['code','title',"author","price","image_url"]