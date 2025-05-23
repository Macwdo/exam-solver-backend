from rest_framework import serializers

from app.models import Exam


class CreateDocumentRequest(serializers.Serializer):
    file_path = serializers.CharField()


class GetPresignedUrlRequest(serializers.Serializer):
    file_path = serializers.CharField()
    file_type = serializers.CharField()


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ["id", "name", "status", "answer"]
