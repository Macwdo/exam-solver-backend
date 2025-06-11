from rest_framework import serializers

from app.models import Exam


class CreateDocumentRequest(serializers.Serializer):
    file = serializers.CharField()


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            "id",
            "name",
            "label",
            "status",
            "answer",
            "date",
            "is_blocked",
        ]
