from rest_framework import serializers

from .models import Course, Lesson
# from users.serializers import UserSerializer


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonsSerializer(source='lesson_set', many=True, required=False)
    # owner = UserSerializer(source='user_set', many=True, required=False)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instance):
        if instance.lesson_set.all().last():
            return instance.lesson_set.all().count()
        return 0

    def get_validation_exclusions(self):
        exclusions = super(CourseSerializer, self).get_validation_exclusions()
        return exclusions + ['owner']
