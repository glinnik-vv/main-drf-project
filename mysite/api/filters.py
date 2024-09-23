import django_filters
from .models import Post, Category, UploadFile, Patient
from django_filters import rest_framework as filters


class PostFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)

        self.filters['category'].field.choices = Category.objects.values_list('id', 'name')

        self.filters['category'].field.empty_label = 'Все категории'

        self.filters['category'].field.widget.attrs.update({'class': 'form-control', 'id': 'category-select'})

        self.filters['title'].field.widget.attrs.update({'class': 'form-control', 'id': 'title-input'})
 

class PatientFilter(filters.FilterSet):
    id_pac = django_filters.CharFilter(field_name='id', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = Patient
        fields = ['id_pac', 'first_name', 'last_name']
