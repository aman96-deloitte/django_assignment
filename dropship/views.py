from django.http import JsonResponse
from rest_framework import status

from .models import Project
from .serializers import ProjectSerializer,UserSerializer,IssueSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .models import Issue
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework.decorators import api_view



# project APIs
class ProjectList(APIView):
    def get(self,request):
        project = Project.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self,request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "error": "not saved"
            })


class ProjectView(APIView):
    def get(self, request, id):
        try:
            project = Project.objects.get(pk=id)
        except Project.DoesNotExcist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self,request,id):
        try:
            project = Project.objects.get(pk=id)
        except Project.DoesNotExcist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            project = Project.objects.get(pk=id)
        except Project.DoesNotExcist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# Issues APIs

class IssueList(APIView):
    def get(self,request):
        issue = Issue.objects.all()
        serializer = IssueSerializer(issue, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self,request):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "error": "not saved"
            })


class IssueView(APIView):
    def get(self, request, id):
        try:
            issue = Issue.objects.get(pk=id)
        except Issue.DoesNotExcist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def put(self,request,id):
        try:
            issue = Issue.objects.get(pk=id)
        except Issue.DoesNotExcist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            issue = Issue.objects.get(pk=id)
        except Issue.DoesNotExcist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







#Issues under a project

class ProjectIssue(APIView):
    def get(self, request, id):
        project = Project.objects.get(pk=id)
        issue = Issue.objects.filter(project=project)
        serializer = IssueSerializer(issue, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, id):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message":"failed"
            })




class LoginView(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username = username).first()
        if user is None:
            raise AuthenticationFailed('Not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')


        payload = {
            'id': user.id,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data={
            'jwt' : token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')

        user = User.objects.filter(id= payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)





















