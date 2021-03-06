import datetime

from django.urls import reverse

import pytest

from faker import Faker
from rest_framework import status

from limits.factories import LimitDateInfoFactory
from limits.models import LimitDateInfo

faker = Faker()


@pytest.mark.django_db
class TestLimitViewSet:

    def test_list(self, api_client):
        url = reverse('limits-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_retrieve(self, api_client):
        limit_info = LimitDateInfoFactory()

        url = reverse('limits-detail', kwargs={'pk': limit_info.id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, dict)

    @pytest.mark.freeze_time
    def test_retrieve_latest(self, api_client, freezer):
        limit_info = LimitDateInfoFactory()

        # Create old limit info
        limit = limit_info.limit
        current_date = datetime.date.today() - datetime.timedelta(days=30)
        for _ in range(5):
            current_date += datetime.timedelta(days=1)
            freezer.move_to(current_date)
            LimitDateInfoFactory(limit=limit)

        url = reverse('limits-latest-retrieve')
        response = api_client.get(url)

        # retrieve latest data info from table
        limit_info_latest = LimitDateInfo.objects.latest('date')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['date'] == limit_info_latest.date.strftime('%Y-%m-%d')
        assert response.data['limit']['id'] == limit_info_latest.limit_id

    def test_filtering_by_date(self, api_client, freezer):
        TODAY_LIMITS_COUNT = 5
        # create today limit infos
        LimitDateInfoFactory.create_batch(TODAY_LIMITS_COUNT)

        # Create old limit infos
        today = datetime.date.today()
        past_date = today - datetime.timedelta(days=30)
        freezer.move_to(past_date)
        LimitDateInfoFactory.create_batch(TODAY_LIMITS_COUNT)

        url = reverse('limits-list')
        params = {'date': today.strftime('%Y-%m-%d')}
        response = api_client.get(url, params)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == TODAY_LIMITS_COUNT

    def test_filtering_by_limit_year(self, api_client):
        limit_info = LimitDateInfoFactory.create_batch(5)[0]

        url = reverse('limits-list')
        params = {'limit__year': limit_info.limit.year}
        response = api_client.get(url, params)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 1
