from rest_framework import serializers

from server.apps.payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    contributor = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Payment
        fields = (
            "collect",
            "sum",
            "created_at",
            "contributor",
        )

    def create(self, validated_data):
        validated_data["contributor"] = self.context["request"].user
        return super().create(validated_data)
