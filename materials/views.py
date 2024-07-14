from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import Course, Lesson, SubForCourseUpdate
from .paginators import MaterialPaginator
from .permissions import IsModer, IsOwner, IsModerOrOwner
from .serializers import CourseSerializer, LessonsSerializer
from .forms import UpdateLessonForm
from materials.tasks import sending_mails


# from django.contrib.auth.models import Group

# users = User.objects.prefetch_related('groups')
#
#
# def user_in_editors(user):
#     groups = user.groups.all()
#     print('Editors' in [group.name for group in groups])


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [AllowAny]
    pagination_class = MaterialPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         permission_classes = [IsAdminUser | IsOwner]
    #     elif self.action == 'list':
    #         permission_classes = [IsAuthenticated]
    #     elif self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsModer]
    #     elif self.action == 'destroy':
    #         permission_classes = [IsAdminUser | IsOwner]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]


class CourseUpdateAPIViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [AllowAny]

    def get_object(self):
        print('запускаю рассылку')
        sending_mails.delay(pk=self.kwargs['pk'])


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonsSerializer
    permission_classes = [AllowAny]

    # def perform_create(self, serializer):
    #     new_lesson = serializer.save()
    #     new_lesson.owner = self.request.user
    #     new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny] # AllowAny
    # pagination_class = MaterialPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated | IsModerOrOwner]
    permission_classes = [AllowAny]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAdminUser | IsModerOrOwner]
    permission_classes = [AllowAny]
    form = UpdateLessonForm


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    # permission_classes = [IsAdminUser | IsOwner]
    permission_classes = [AllowAny]


class SubscriptionAPIView(generics.CreateAPIView):
    queryset = SubForCourseUpdate.objects.all()
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get(Course.pk)
        course_item = get_object_or_404(Course, id=course_id)

        subscription, created = SubForCourseUpdate.objects.get_or_create(user=user, course=course_item)
        if not created:
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message})
