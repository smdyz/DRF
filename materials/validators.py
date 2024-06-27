from rest_framework.serializers import ValidationError


class UrlsValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        val = dict(value).get(self.field)
        if val is not None and len(val) > 0 and val[:23] != 'https://www.youtube.com':
            raise ValidationError('Ссылка содержит недопустимые значения: '
                                  'возможно вы ошиблись или вставили ссылку на личный сайт или стороннюю '
                                  'образовательную платформу')
