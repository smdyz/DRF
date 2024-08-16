from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from .models import Product, Category, SubForProductUpdate
from .paginators import MaterialPaginator
#  from .permissions import IsModer, IsOwner, IsModerOrOwner
from .serializers import ProductSerializer, CategorySerializer
from .forms import UpdateProductForm
from materials.tasks import sending_mails


# from django.contrib.auth.models import Group

# users = User.objects.prefetch_related('groups')
#
#
# def user_in_editors(user):
#     groups = user.groups.all()
#     print('Editors' in [group.name for group in groups])


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
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


class CategoryUpdateAPIViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [AllowAny]

    def get_object(self):
        print('запускаю рассылку')
        sending_mails.delay(pk=self.kwargs['pk'])


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    # def perform_create(self, serializer):
    #     new_Product = serializer.save()
    #     new_Product.owner = self.request.user
    #     new_Product.save()


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [AllowAny]     # AllowAny
    # pagination_class = MaterialPaginator


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # permission_classes = [IsAuthenticated | IsModerOrOwner]
    permission_classes = [AllowAny]


class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # permission_classes = [IsAdminUser | IsModerOrOwner]
    permission_classes = [AllowAny]
    form = UpdateProductForm


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    # permission_classes = [IsAdminUser | IsOwner]
    permission_classes = [AllowAny]


class SubscriptionAPIView(generics.CreateAPIView):
    queryset = SubForProductUpdate.objects.all()
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        user = self.request.user
        product_id = self.request.data.get(Product.pk)
        product_item = get_object_or_404(Product, id=product_id)

        subscription, created = SubForProductUpdate.objects.get_or_create(user=user, product=product_item)
        if not created:
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message})
