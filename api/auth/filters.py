from django_filters import rest_framework as filters
from account.models import User


class UserFilter(filters.FilterSet):

    head = filters.ModelChoiceFilter(queryset=User.objects.filter(role=User.HEAD), 
                field_name='points_as_staff', lookup_expr='head')

    class Meta:
        model = User
        fields = [
            'head',
            'role',
            'is_active', 
            'group',
        ]