from django.contrib.auth.models import Group
from utils.responses import RESPONSE_CODES
from utils.restful_responses import send_response
from userapi.models import User
from rest_framework import generics
from django.contrib.auth.models import update_last_login
from userapi.api.serializers import UserSignUpSerializer,UserSerializer
from rest_framework_jwt.settings import api_settings
import jwt
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


""" This api requires first_name,last_name,email,password and role for signup,on the basis of email it create the user
 group acc to role and save password in db in hash"""
class UserSignUpView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def create(self,request,*args,**kwargs):
        email = request.data.get('email')     
        user = User.objects.filter(email=email).first()
        if not user:            
          serializer = UserSignUpSerializer(data=request.data)
          if serializer.is_valid():
              instance = serializer.save()    
              group, created = Group.objects.get_or_create(name=instance.role)
              group.user_set.add(instance)                        
              return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Request was successful.',
                                 )
          else:
              return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)
                       
        else:
             return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                             ui_message='user with this email has been already registered')



"""This api requires two params email and new_password and save the new password in the db"""
class ForgotPasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def update(self,request,*args,**kwargs):
        try:
          user = User.objects.get(email=request.data.get('email'))
        except:
             return send_response(response_code=RESPONSE_CODES['FAILURE'],
                                 developer_message='User with this email does not exist')
        user.set_password(request.data.get('new_password'))

        return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='password is successfully changed.')


"""This Api returns the Json Web Token to the user after checking email and password"""
class UserLoginView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
   
    def create(self,request,*args,**kwargs):
         email = request.data.get('email',None)
         password = request.data.get('password',None)
         user = User.objects.get(email=email)
         print(user)
         valid = user.check_password(password)                             
         if valid:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)                                 
            data = { 'token':jwt_token }
            
            return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Request was successful.',data=data)      
         else:
             return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                             ui_message='user with this given email does not exist')


"""This Api returns the student information added by the teacher and requires first_name,last_name,email to add 
student and uses Jwt for authentication"""
class TeacherAddStudentView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self,request,*args,**kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save(role='teacher')
            group, created = Group.objects.get_or_create(name=instance.role)
            group.user_set.add(instance)
            return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Student is successfully added.',
                                 )
        else:
            return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)
                       

"""This Api return the list of all students added by the teacher and uses Jwt so that only teacher can access this data"""
class StudentListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self,request,*args,**kwargs):
        role = User.objects.filter(role='teacher')
        serializer = UserSerializer(instance=role,many=True)                  
        data = serializer.data
        return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Request was successful.',data=data)


"""This Api returns the particular student data and requires jwt to authenticate the student"""
class StudentDetailView(generics.ListAPIView):

  queryset = User.objects.all()
  serializer_class = UserSerializer
  authentication_classes = (JSONWebTokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def list(self,request,*args,**kwargs):
      user = request.user
      instance = User.objects.get(id=user.id)
      serializer = UserSerializer(instance=instance)
      data = serializer.data
      return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Request was successful.',data=data)


"""This Api returns the data of the user that is added by admin and uses JWT"""
class AdminAddUserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self,request,*args,**kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save(role='admin')
            group, created = Group.objects.get_or_create(name=instance.role)
            permission = Permission.objects.get('auth.add_user')
            group.user_permission.add(permission)
            group.user_set.add(instance)
            return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Student is successfully added.',
                                 )
        else:
            return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)


"""This Api returns the List of all the Users that is added by admin"""
class UserListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self,request,*args,**kwargs):
        role = User.objects.filter(role='admin')
        serializer = UserSerializer(instance=role,many=True)                  
        data = serializer.data
        return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Request was successful.',data=data)                             