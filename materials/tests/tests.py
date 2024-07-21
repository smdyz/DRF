from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson
from materials.forms import UpdateLessonForm
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user('smidy', 't.z@mail.ru', 'Qw1')
        self.user = User.objects.get(username='smidy')
        self.form = UpdateLessonForm
        Lesson.objects.create(name='test', description='test')
        self.lesson = Lesson.objects.get(name='test')

    def test_create_lesson(self):
        """ Тестирование создания урока """
        data = {'name': 'test', 'description': 'test'}

        response = self.client.post(
            '/lesson/create/',
            data=data,
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEquals(
            response.json(),
            {'id': 2, 'name': 'test', 'preview': None, 'description': 'test', 'url': None, 'course': None,
             'owner': None}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lessons(self):
        """Тестирование вывода списка уроков"""

        response = self.client.get(
            '/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            [{'id': 4, 'name': 'test', 'preview': None, 'description': 'test', 'url': None, 'course': None,
                'owner': None}]
        )

    def test_retrieve_lesson(self):
        """Тестирование вывода урока"""

        response = self.client.get(f'/lesson/{self.lesson.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': 5, 'name': 'test', 'preview': None, 'description': 'test', 'url': None, 'course': None,
             'owner': None}
        )

    def test_update_lesson(self):
        """Тестирование обновления уроков"""

        response = self.client.patch(f'/lesson/update/{self.lesson.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        form = self.form({
            'name': 'test lesson',
            'description': 'test lesson'
        }, instance=self.lesson)

        self.assertTrue(form.is_valid())

        form.save()

        self.assertEquals(self.lesson.name, 'test lesson')
        self.assertEquals(self.lesson.description, 'test lesson')

    def test_delete_lesson(self):
        """Тестирование обновления уроков"""

        response = self.client.delete(f'/lesson/delete/{self.lesson.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEquals(Lesson.objects.count(), 0)

        # self.assertRedirects(response, expected_url='/lesson/')


class SubTestCase(APITestCase):
    def setUp(self):
        pass
