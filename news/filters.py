from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from .models import Post, Category, PostCategory
from django.forms import DateInput


class PostFilter(FilterSet):
    Tag = ModelMultipleChoiceFilter(
        field_name='PostCategory__category',
        queryset=Category.objects.all(),
        label='tags',
        conjoined=False,
    )

    TimeAdding = DateFilter(
        'date_post',
        lookup_expr='gt',
        label='Дата не раньше',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
