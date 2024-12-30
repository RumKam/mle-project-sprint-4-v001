# Подготовка виртуальной машины

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/RumKam/mle-project-sprint-4-v001.git
```

## Активируйте виртуальное окружение

Создать новое виртуальное окружение можно командой:

```
python3 -m venv env_recsys_start
```

После его инициализации следующей командой

```
. env_recsys_start/bin/activate
```

установите в него необходимые Python-пакеты следующей командой

```
pip install -r requirements.txt
```

### Скачайте файлы с данными

Для начала работы понадобится три файла с данными:
- [tracks.parquet](https://storage.yandexcloud.net/mle-data/ym/tracks.parquet)
- [catalog_names.parquet](https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet)
- [interactions.parquet](https://storage.yandexcloud.net/mle-data/ym/interactions.parquet)
 
Скачайте их в директорию локального репозитория. Для удобства вы можете воспользоваться командой wget:

```
wget https://storage.yandexcloud.net/mle-data/ym/tracks.parquet

wget https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet

wget https://storage.yandexcloud.net/mle-data/ym/interactions.parquet
```

## Запустите Jupyter Lab

Запустите Jupyter Lab в командной строке

```
jupyter lab --ip=0.0.0.0 --no-browser
```

# Расчёт рекомендаций

Код с описанием получения рекомендаций первой части проекта находится в файле `mle-project-sprint-4-v001/recommendations_v1.ipynb`. Для тестирования сервиса рассчитывать рекомендации не нужно.

# Сервис рекомендаций

Поскольку файлы с рекомендациями достаточно объемные, необходимые для тестирования сервиса на нескольких пользователях рекомендации находятся в файлах `test_recommendations.parquet` и `test_top_popular.parquet` в папке recsys/recommendations.

1. Необходмо перейти в папку сервиса:
```
cd mle-project-sprint-4-v001/recsys
```
2. В первом терминале необходимо запустить сервис для генерации онлайн-рекомендаций на основе сходства музыкальных треков:
```
uvicorn features_service:app --port 8010
```
3. Во втором терминале необходимо запустить сервис для добавления онлайн-событий в онлайн-историю пользователя:
```
uvicorn events_service:app --port 8020
```
4. В третьем терминале необходимо запустить основное приложение, которое генерирует рекомендации всех типов:
```
uvicorn recommendation_service:app
```

# Инструкции для тестирования сервиса

Для тестиования сервиса необходимо в отдельном терминале запустить из корневой директории:
```
python test_service.py
```
Логи хранятся файле `test_service.log`

#  Cтратегия смешивания онлайн- и офлайн-рекомендаций

В основном коде приложения `recommendation_service.py` реализован алгорим, который работает по следующей схеме: если у пользователя есть онлайн-история, то его окончательные рекомендации формируются путем сочетания онлайн- и офлайн-рекомендаций. При этом онлайн-рекомендации размещаются на нечетных позициях, а офлайн-рекомендации — на четных.
