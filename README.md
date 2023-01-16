# yamdb_final

![master](https://github.com/hlamida/yamdb_final/workflows/yamdb_workflow/badge.svg)

### Предназначение проекта:

Проект YaMDb через API собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://git@github.com:Hlamida/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

Активировать виртуальное окружение:

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Тестирование:

В проекте есть возможность заполнить базу данных для тестирования csv-файлами. Для этого можно использовать имеющиеся или перенести свои файлы в директорию api_yamdb\static\data.

Заполнить базу данных контентом из приложенных csv-файлов:

```
python3 manage.py importcsv
```

Запуск тестов:

```
pytest
```

### Примеры:

Примеры и полная документация для API YaMDb содержится по адресу http://127.0.0.1:8000/redoc/.
Документация представлена в формате Redoc.

### Технологии:

Проект сделан на Django и DRF.

### Об авторах:

Авторы: Александр Кулагин (начальник отдела разработки, ссылка на GitHub https://github.com/Hlamida), Сергей Фадеев (главный специалист отдела разработки, ссылка на GitHub https://github.com/s-fadeev), Шушаркин Герман (ведущий специалист отдела разработки, ссылка на GitHub https://github.com/shusharkin).
