from rest_framework import serializers
from .models import Mission, MissionImage
from accounts.models import User

class MissionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionImage
        fields = ['id', 'image']

class MissionSerializer(serializers.ModelSerializer):
    publisher_nickname = serializers.CharField(source='publisher.nickname', read_only=True)
    acceptor_nickname = serializers.CharField(source='acceptor.nickname', read_only=True)
    images = MissionImageSerializer(many=True, read_only=True)

    class Meta:
        model = Mission
        fields = [
            'id', 'title', 'content', 'reward_score',
            'status', 'is_draft', 'publisher', 'publisher_nickname',
            'acceptor', 'acceptor_nickname', 'images',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['publisher', 'acceptor', 'status', 'is_draft']

class MissionDraftSerializer(serializers.ModelSerializer):
    images = MissionImageSerializer(many=True, read_only=True)

    class Meta:
        model = Mission
        fields = ['id', 'title', 'content', 'reward_score', 'is_draft', 'images']

    def create(self, validated_data):
        validated_data['is_draft'] = True
        validated_data['status'] = 'draft'
        return super().create(validated_data)

class MissionPublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['title', 'content', 'reward_score']

    def validate(self, attrs):
        if not attrs.get('title') or not attrs.get('content'):
            raise serializers.ValidationError("标题和内容不能为空")
        return attrs

class MissionAcceptSerializer(serializers.Serializer):
    def validate(self, mission):
        if mission.status != 'pending':
            raise serializers.ValidationError("只有待接取委托可接取")
        if mission.publisher == self.context['request'].user:
            raise serializers.ValidationError("不能接取自己的委托")
        return mission

class MissionCompleteSerializer(serializers.Serializer):
    def validate(self, mission):
        if mission.status != 'in_progress':
            raise serializers.ValidationError("只有进行中委托可完成")
        return mission