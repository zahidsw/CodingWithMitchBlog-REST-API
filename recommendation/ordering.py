from rest_framework.filters import OrderingFilter

class MyCustomOrdering(OrderingFilter):
    allowed_custom_filters = ['testMethod']

    def get_ordering(self, request, queryset, view):
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        print("test")
        params = request.query_params.get(self.ordering_param)

        if params:
            fields = [param.strip() for param in params.split(',')]
            # care with that - this will alow only custom ordering!
            ordering = [f for f in fields if f in self.allowed_custom_filters]
            if ordering:
                return ordering

        # No ordering was included, or all the ordering fields were invalid
        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):

        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            # implement a custom ordering here
            ordering = ['-id']

        if ordering:
            return queryset.order_by(*ordering)

        return queryset