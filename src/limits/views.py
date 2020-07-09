from django.db import models
from django.db.models import Case, Q, Sum, When

from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from contracts.serializers import ContractSerializer

from core.viewset_mixins import SerializerMapMixin

from limits.models import LimitDateInfo, Source
from limits.serializers import LimitDateInfoSerializer, SourceSerializer

from tenders.models import Tender
from tenders.serializers import TenderSerializer


class LimitViewSet(ReadOnlyModelViewSet):
    queryset = LimitDateInfo.objects.all().order_by('date') \
        .select_related('limit')
    serializer_class = LimitDateInfoSerializer
    filterset_fields = ('date', 'limit__year')

    @action(detail=False, url_path='latest', url_name='latest-retrieve',
            methods=('get',))
    def latest_object_retrieve(self, *args, **kwargs):
        try:
            instance = self.get_queryset().latest('date')
        except LimitDateInfo.DoesNotExist:
            raise NotFound('No any records in the table')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SourceViewSet(SerializerMapMixin, ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    serializer_class_map = {
        'contracts': ContractSerializer,
        'tenders': TenderSerializer,
    }

    @action(detail=True, url_path='contracts', url_name='contacts',
            methods=('get',))
    def contracts(self, request, **kwargs):
        source = self.get_object()
        contracts = self._get_contracts_queryset(source)
        serializer = self.get_serializer(contracts, many=True)
        return Response(serializer.data)

    def _get_contracts_queryset(self, source):
        """
        Return contracts with amount
        """
        source_id_equal = Q(
            contractprice__limit__industry_code__limit_article__source_id=source.id)  # noqa: E501
        return source.contracts.annotate(
            money=Case(
                When(source_id_equal,
                     then=Sum('contractprice__money', distinct=True)),
                output_field=models.DecimalField(),
            ),
            delta=Case(
                When(source_id_equal,
                     then=Sum('contractprice__contractpricechange__delta',
                              distinct=True)),
                output_field=models.DecimalField(),
            ),
        )

    @action(detail=True, url_path='tenders', url_name='tenders',
            methods=('get',))
    def tenders(self, request, **kwargs):
        limit = self.get_object()
        tenders = self._get_tenders_queryset(limit)
        serializer = self.get_serializer(tenders, many=True)
        return Response(serializer.data)

    def _get_tenders_queryset(self, source):
        """
        Return tenders in process with amount
        """
        source_id_equal = Q(
            startprice__limit__industry_code__limit_article__source_id=source.id)  # noqa: E501
        return source.tenders.filter(status=Tender.Status.IN_WORK).annotate(
            money=Case(
                When(source_id_equal, then=Sum('startprice__money')),
                output_field=models.DecimalField(),
            ),
        )
