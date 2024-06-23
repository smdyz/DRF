from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Course, Lesson
from .permissions import IsModer, IsOwner, IsModerOrOwner
from .serializers import CourseSerializer, LessonsSerializer


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsAdminUser | IsOwner]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsModer]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser | IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonsSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsModer]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsModerOrOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsModerOrOwner]


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsOwner]
