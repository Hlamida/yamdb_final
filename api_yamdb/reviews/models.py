from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from reviews.constants import (ADMIN, MAXSCORE, MINSCORE, MODERATOR,
                               ROLE_CHOICES, STUFF, TEXT_LEN, USER)
from reviews.validators import validate_username, validate_year


class User(AbstractUser):
    """Определяет модель пользователя."""

    username = models.CharField(
        validators=([validate_username]),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(
        'Bio',
        blank=True,
    )
    role = models.CharField(
        'Role',
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    confirmation_code = models.CharField(
        'Confirmation code',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX',
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_stuff(self):
        return self.role == STUFF

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def post(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.confirmation_code = confirmation_code
        instance.save()


class Category(models.Model):
    """Модель описывает категории, например, книги, фильмы, музыка."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель описывает жанры, например, сказка, рок, артхаус."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель описывает произведение."""

    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[validate_year])
    description = models.CharField(max_length=256)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связи жанров с произведениями."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    """Модель отзыва о произведении."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
    )
    text = models.CharField(
        max_length=250,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(
                MINSCORE,
                message=f'Оценка не может быть меньше {MINSCORE}',
            ),
            MaxValueValidator(
                MAXSCORE,
                message=f'Оценка не может быть больше {MAXSCORE}',
            ),
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_review',
            )]
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LEN]


class Comment(models.Model):
    """Модель для комментариев к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.CharField(
        max_length=250,
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TEXT_LEN]
