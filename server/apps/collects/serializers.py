from rest_framework import serializers

from server.apps.collects.models import Collect, Occasion


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ("id", "name")


class CollectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    current_sum = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )
    contributors_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Collect
        fields = (
            "name",
            "author",
            "description",
            "occasion",
            "current_sum",
            "final_sum",
            "created_at",
            "completion_datetime",
            "contributors_count",
            "image",
        )
        read_only_fields = ("author", "created_at")
