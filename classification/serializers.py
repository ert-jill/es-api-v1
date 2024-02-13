from rest_framework import serializers
from classification.models import Classification
from user.tokens import User

class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = [
            'id',
            'name',
            'description',
            'parent',
            'depth',
        ]
        read_only_fields = (
            'id',
            'depth',
        )
        ref_name = 'Classification'

    def create(self, validated_data):
        if validated_data.get('parent') is None:
            validated_data['depth'] = 0;
        else :
            parent = Classification.objects.get(id = validated_data.get('parent').id )
            validated_data['depth'] = parent.depth+1;
        return super().create(validated_data)