from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class BasicArticlePagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

class CustomArticlePagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_page_size(self, request):
        if self.page_size_query_param and self.page_size_query_param in request.query_params:
            param_value = request.query_params[self.page_size_query_param]
            try:
                val = int(param_value)
            except (TypeError, ValueError):
                raise ValidationError({
                    'page_size': 'Invalid page_size. Must be a valid positive integer.'
                })
            if val <= 0:
                raise ValidationError({
                    'page_size': 'Invalid page_size. Value must be greater than 0.'
                })
            if self.max_page_size and val > self.max_page_size:
                return self.max_page_size
            return val
        return self.page_size

    def get_paginated_response(self, data):
        return Response({
            'page_info': {
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'items_info': {
                'total_items': self.page.paginator.count,
                'page_items_count': len(data),
                'page_size': self.get_page_size(self.request),
            },
            'results': data
        })
