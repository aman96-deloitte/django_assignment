from django.http import JsonResponse
from .models import Project
from .serializers import ProjectSerializer

def project_list(request):

    project = Project.objects.all()
    serializer = ProjectSerializer(project, many= True)
    return JsonResponse(serializer.data, safe=False)
