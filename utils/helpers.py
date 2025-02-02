from django.db.models import Q

class QuerysetHelper:
    @staticmethod
    def apply_filters(queryset, filterset_class, params):
        if filterset_class:
            filterset = filterset_class(params, queryset=queryset)
            if filterset.is_valid():
                return filterset.qs
        return queryset

    @staticmethod
    def apply_search(queryset, search_query, fields):
        if search_query:
            queries = Q()
            for field in fields:
                queries |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(queries).distinct()
        return queryset

    @staticmethod
    def apply_ordering(queryset, ordering):
        if ordering:
            return queryset.order_by(ordering)
        return queryset

