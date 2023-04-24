from rest_framework import mixins, viewsets


class GetListCreateDeleteViewSet(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    pass
