from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UploadedFile
from .serializers import UploadedFileSerializer

class UserFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        files = UploadedFile.objects.filter(user=user)
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data)
