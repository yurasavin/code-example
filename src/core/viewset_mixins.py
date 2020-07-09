class SerializerMapMixin:
    """
    This mixin allows to specify custom serializer class for any particular
     `action`.

     Example:
        >>> class UserViewSet(SerializerMapMixin, ...):
        ...     serializer_class = UserGenericSerializer
        ...     serializer_class_map = {
        ...         'create': UserCreateSerializer,
        ...         'activate': UserActivateSerializer,
        ...     }


    """
    serializer_class_map = NotImplemented
    action = NotImplemented
    serializer_class = NotImplemented

    def get_serializer_class(self):
        serializer_class = self.serializer_class_map.get(
            self.action, self.serializer_class,
        )
        return serializer_class
