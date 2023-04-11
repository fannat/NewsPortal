from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from .models import Post, Cathegory, PostCathegory
from django.forms import DateInput

class PostFilter(FilterSet):
    Tag = ModelMultipleChoiceFilter(
        field_name = 'postcathegory__cathegory',
        queryset = Cathegory.objects.all(),
        label = 'тэги',
        conjoined = False,
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

    class Meta:
        model = Post
        fields = {
           'head_post': ['icontains'],
        }