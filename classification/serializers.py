from rest_framework import serializers
from classification.models import Classification
from user.tokens import User


class ClassificationSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset= Classification.objects.all(), required = False)

    class Meta:
        model = Classification
        fields = [
            "id",
            "name",
            "description",
            "parent",
            "depth",
        ]
        read_only_fields = ("id","depth",)
        ref_name = "Classification"

    def create(self, validated_data):
        if validated_data.get("parent") is None:
            validated_data["depth"] = 0
        else:
            validated_data["depth"] = validated_data.get("parent").depth + 1
        return super().create(validated_data)
