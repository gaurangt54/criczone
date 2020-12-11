import django_filters
from django_filters import *
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    notes = CharFilter(field_name="notes", lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']

class ProductFilter(django_filters.FilterSet):
    #minimum_price = NumberFilter(field_name="price", lookup_expr='gte')
    #maximum_price = NumberFilter(field_name="price", lookup_expr='lte')
    sname = CharFilter(field_name="name", lookup_expr='icontains')

    #minimum_price.label = "Minimum Price"
    #maximum_price.label = "Maximum Price"

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['name','price','description','date_created','image','tags','category']
    
