from api.filters import TitlesFilter
from api.permissions import (IsAdminOnly, IsAdminUserOrReadOnly,
                             IsOwnerAdminModeratorOrReadOnly)
from api.serializers import (AdminSerializer, CategoriesSerializer,
                             CommentsSerializer, GenresSerializer,
                             GetTokenSerializer, NotAdminSerializer,
                             ReadTitlesSerializer, ReviewsSerializer,
                             SignupSerializer, WriteTitlesSerializer)
from api.utils import CategoryGenreMixin
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User


class CategoriesViewSet(CategoryGenreMixin):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CategoryGenreMixin):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        """Выбор нужного сериализатора в зависимости от вида запроса."""

        if self.action in ('list', 'retrieve'):
            return ReadTitlesSerializer

        return WriteTitlesSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """Работа с пользователями."""

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAuthenticated, IsAdminOnly,)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        """Получение информации о пользователе."""

        serializer = AdminSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = AdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data)


class APIGetToken(APIView):
    """Получение токена по коду подтверждения."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь отсутствует.'},
                status=status.HTTP_404_NOT_FOUND)

        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token

            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)

        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """Отправка кода подтверждения на почту пользователя."""

    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email='hlamida@gmail.com',
            to=[data['to_email']],
        )
        email.send()

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Confirmation API code: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Confirmation API code.',
        }
        self.send_email(data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerAdminModeratorOrReadOnly,
    )

    def _get_title(self):
        """Возвращает произведение, указанное в URL."""

        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'),
        )

    def get_queryset(self):
        """Возвращает QuerySet с отзывами."""

        return self._get_title().reviews.all()

    def perform_create(self, serializer):
        """Передает сериализатору автора и произведение из запроса."""

        serializer.save(
            author=self.request.user,
            title=self._get_title(),
        )


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerAdminModeratorOrReadOnly,
    )

    def _get_review(self):
        """Возвращает отзыв из запроса."""

        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
        )

    def get_queryset(self):
        """Возвращает QuerySet с комментариями."""

        return self._get_review().comments.all()

    def perform_create(self, serializer):
        """Передает сериализатору автора коммента и отзыв из запроса."""

        serializer.save(
            author=self.request.user,
            review=self._get_review(),
        )
