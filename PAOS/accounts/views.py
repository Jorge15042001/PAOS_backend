#  from django.shortcuts import render
from django.contrib.auth import authenticate, login
#  from django.views.decorators.csrf import csrf_exempt

#  from django.http import HttpResponse
#  import json

from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework import status
#  from rest_framework import permissions

from .serializers import PAOSUserSerializer

# Create your views here.


class APILogin (APIView):
    def get(self, request):
        '''
        '''
        return Response({"success": True,
                         "authenticated": request.user.is_authenticated})

    def post(self, request, *args, **kwargs):
        '''
            login
                username: string with username
                password: string with password
        '''
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        if username and password:
            # Test username/password combination
            print("before authenticate")
            user = authenticate(username=username, password=password)
            # Found a match
            if user is not None:
                # User is active
                if user.is_active:
                    # Officially log the user in
                    print("before login")
                    login(self.request, user)
                    user_data = PAOSUserSerializer(user).data
                    print(request.user.is_authenticated)
                    print("successfull login")
                    return Response(
                        {'success': True, "user-data": user_data},
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {'success': False, 'error': 'User is not active'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response(
                {'success': False, 'error': 'Wrong username and/or password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'success': False, 'error': 'missing fields'},
            status=status.HTTP_400_BAD_REQUEST
        )


class APISignup (APIView):
    def post(self, request, *args, **kwargs):
        '''
            signup
                username: string with username
                email: string with user's email
                password1: string with password
                password2: string with password
                first_name: user's first name
                last_name: user's last name
        '''
        new_user_data = {
            "username": request.data.get('username'),
            "password1": request.data.get('password1'),
            "password2": request.data.get('password2'),

            "email": request.data.get('email'),
            "first_name": request.data.get('first_name'),
            "last_name": request.data.get('last_name')
        }
        new_user = PAOSUserSerializer(data=new_user_data)
        #  print(new_user.errors)
        if not new_user.is_valid():
            return Response(
                {'success': False, 'error': list(
                    new_user.errors.values())[0][0]},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (new_user_data["password1"] and new_user_data["password2"]):
            return Response(
                {'success': False, 'error': "missing passwords"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_user_data["password1"] != new_user_data["password2"]:
            return Response(
                {'success': False, 'error': "password mismatch"},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_user = new_user.save()
        new_user.set_password(new_user_data["password2"])
        new_user.save()

        return Response(
            {'success': True, },
            status=status.HTTP_200_OK
        )
