from rest_framework import serializers

from .models import Category, Product
from .validators import UrlsValidator


# from users.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        validators = [UrlsValidator(field='url')]


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField(read_only=True)
    products = ProductSerializer(source='product_set', many=True, required=False, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def get_product_count(self, instance):
        if instance.lesson_set.all().last():
            return instance.lesson_set.all().count()
        return 0

    def get_validation_exclusions(self):
        exclusions = super(CategorySerializer, self).get_validation_exclusions()
        return exclusions + ['owner']
