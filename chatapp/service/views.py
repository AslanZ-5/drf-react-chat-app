from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Service
from .schema import service_list_docs
from .serializer import ServiceSerializer


class ServiceListViewSet(viewsets.ViewSet):
    # Получаем все объекты модели Service
    queryset = Service.objects.all()

    # Декоратор для документации API
    @service_list_docs
    def list(self, request):
        """
        Возвращает список услуг с возможностью фильтрации по различным параметрам
        """
        # Получаем параметры запроса из URL
        category = request.query_params.get("category")  # Фильтрация по категории
        qty = request.query_params.get("qty")  # Ограничение количества результатов
        by_user = (
            request.query_params.get("by_user") == "true"
        )  # Фильтрация по пользователю
        by_serviceid = request.query_params.get(
            "by_serviceid"
        )  # Фильтрация по ID услуги
        with_num_members = request.query_params.get(
            "with_num_members"
        )  # Включить количество участников

        # Проверка аутентификации пользователя для определенных запросов
        if by_user or by_serviceid and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # Фильтрация по категории
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Фильтрация по пользователю
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        # Ограничение количества результатов
        if qty:
            self.queryset = self.queryset[: int(qty)]

        # Аннотация количества участников
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Фильтрация по ID услуги и проверка наличия услуги
        if by_serviceid:
            try:
                self.queryset = self.queryset.filter(id=by_serviceid)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Service with id {by_serviceid} not found"
                    )
            except ValueError:
                raise ValidationError(detail="Service value error")

        # Сериализация результатов и возврат ответа
        serializer = ServiceSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
