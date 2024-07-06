from rest_framework import generics, pagination


class Base_Create(generics.CreateAPIView):
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()


class Base_Update(generics.UpdateAPIView):
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()


class Base_Retrieve(generics.RetrieveAPIView):
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()


class Base_Destroy(generics.DestroyAPIView):
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"


class Base_List(generics.ListAPIView):
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
