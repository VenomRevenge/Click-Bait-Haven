from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from articles.models import Article, Tag
from api.serializers import ArticleSerializer, SingleArticleSerializer, TagSerializer
from rest_framework.generics import RetrieveAPIView


class ListArticles(ListAPIView):
    """
    API view to fetch all articles with optional filtering and ordering.
    Query Parameters supported:
    - `title`: Search articles by title (case-insensitive, partial match).
    - `username`: Search articles by author's username (case-insensitive, partial match).
    - `tag`: Filter articles by tags (multiple `tag` parameters allowed for filtering).
    - `order_by`: Specify the field to order results ('-created_at' and 'created_at').
    Note: To see the contents of the article please fetch it using the 'api/article/{id}' endpoint.
    """
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = (
            Article.objects
            .active_articles()
            .select_related('author__user')
            .prefetch_related('tags')
            .only(
                'id',
                'author__id',
                'author__user__username',
                'picture',
                'title',
                'created_at',
            )
        )

        title_to_search = self.request.query_params.get('title', None)
        if title_to_search:
            queryset = queryset.filter(title__icontains=title_to_search)

        author_to_search = self.request.query_params.get('username', None)
        if author_to_search:
            queryset = queryset.filter(author__user__username__icontains=author_to_search)

        tags_to_search = self.request.query_params.getlist('tag', None)
        if tags_to_search:
            for tag in tags_to_search:
                queryset = queryset.filter(tags__name=tag)

        order_by = self.request.query_params.get('order_by', '-created_at')
        queryset = queryset.order_by(order_by)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveSingleArticle(RetrieveAPIView):
    """
    API view to fetch a single article by its ID showing its content.
    """
    queryset = (
        Article.objects
        .active_articles()
        .select_related('author__user')
        .prefetch_related('tags')
    )
    serializer_class = SingleArticleSerializer
    lookup_field = 'id'

class ViewTags(ListAPIView):
    """
    API view to fetch all currenty available tags.
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
