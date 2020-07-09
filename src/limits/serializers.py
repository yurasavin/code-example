from rest_framework import serializers

from limits.models import Limit, LimitArticle, LimitDateInfo, Source


class LimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Limit
        fields = ('id', 'year')


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('num', 'name', 'limit')


class LimitArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitArticle
        fields = ('name', 'num', 'source')


class LimitDateInfoSerializer(serializers.ModelSerializer):
    limit = LimitSerializer(read_only=True)

    class Meta:
        model = LimitDateInfo
        fields = ('limit', 'data', 'date')
