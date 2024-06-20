from rest_framework import serializers

from .models import Course, Lesson


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonsSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instance):
        if instance.lesson_set.all().last():
            return instance.lesson_set.all().count()
        return 0
