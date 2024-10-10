from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Review
from .serializers import ReviewSerializer
from django_filters import rest_framework as django_filters
from rest_framework.pagination import PageNumberPagination

class ReviewFilter(django_filters.FilterSet):
    """
    Filter for filtering reviews by movie title or rating.
    """
    movie_title = django_filters.CharFilter(field_name='movie_title', lookup_expr='icontains')
    rating = django_filters.RangeFilter()
    class Meta:
        model = Review
        fields = ['movie_title', 'rating']

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Handles creating, retrieving, updating, and deleting movie reviews.
    Filters reviews by movie title and rating, and orders by creation date or rating.
    Only the creator of a review can modify or delete it.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ReviewFilter
    ordering_fields = ['created_at', 'rating']
    ordering = ['-rating']
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        """
        Associates the user who creates the review with it.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Ensures that only the owner of a review can update it.
        """
        review = self.get_object()
        if review.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You can only edit your own reviews.")

    def perform_destroy(self, instance):
        """
        Ensures that only the owner of a review can delete it.
        """
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You can only delete your own reviews.")
