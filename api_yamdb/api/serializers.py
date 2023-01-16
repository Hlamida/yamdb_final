import re

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_year


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(), fields=('username', 'email')
        )
        ]

    def validate_username(self, value):
        """Проверяет username на соответствие требованиям."""

        if re.match(r'^[\\w.@+-]+\\z', value):
            raise serializers.ValidationError(
                'Недопустимые символы в username.'
            )
        if value == 'me':
            raise ValidationError(
                ('Измените имя пользователя.'),
                params={'value': value},
            )
        return value


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор админа."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class NotAdminSerializer(AdminSerializer):
    """Сериализатор пользователя 'не админа'."""

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReadTitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""

    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        model = Title


class WriteTitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения произведений."""

    year = serializers.IntegerField(
        validators=(validate_year,),
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к отзыву."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'review', 'pub_date')
        model = Comment


class ReviewsSerializer(serializers.ModelSerializer):
    """Класс сериализатора для отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ['title']

    def create(self, validated_data):
        """Проверяет существование отзыва на произведение от юзера.
        Если таковой уже есть, выкидывает исключение.
        """

        if Review.objects.filter(
            title=validated_data.get('title'),
            author=validated_data.get('author'),
        ).exists():
            raise serializers.ValidationError(
                'Нельзя добавить больше одного отзыва'
            )

        return super().create(validated_data)
