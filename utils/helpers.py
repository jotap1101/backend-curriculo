from django.db.models import Q

class QuerysetHelper:
    @staticmethod
    def apply_filters(queryset, filterset_class, params):
        filterset = filterset_class(params, queryset=queryset)

        if filterset.is_valid():
            return filterset.qs
        
        return queryset

    @staticmethod
    def apply_search(queryset, search_param, fields):
        if search_param:
            queries = [Q(**{f"{field}__icontains": search_param}) for field in fields]
            query = queries.pop()

            for item in queries:
                query |= item

            return queryset.filter(query)
        
        return queryset

    @staticmethod
    def apply_ordering(queryset, ordering_param):
        if ordering_param:
            return queryset.order_by(ordering_param)
        
        return queryset
