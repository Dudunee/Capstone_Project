from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Review
from .serializers import ReviewSerializer
from django_filters import rest_framework as django_filters

class ReviewFilter(django_filters.FilterSet):
    movie_title = django_filters.CharFilter(field_name='movie_title', lookup_expr='icontains')
    rating = django_filters.RangeFilter()
    class Meta:
        model = Review
        fields = ['movie_title', 'rating']

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ReviewFilter
    ordering_fields = ['created_at', 'rating']
    ordering = ['-rating']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

    def perform_update(self, serializer):
        review = self.get_object()
        if review.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You can only edit your own reviews.")
    
    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You can only delete your own reviews.")
