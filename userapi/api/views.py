from django.contrib.auth.models import Group
from utils.responses import RESPONSE_CODES
from utils.restful_responses import send_response
from userapi.models import User
from rest_framework import generics
from django.contrib.auth.models import update_last_login
from userapi.api.serializers import UserSignUpSerializer
from rest_framework_jwt.settings import api_settings
import jwt

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER



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



class UpdateUserPasswordView(generics.UpdateAPIView):

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



class TeacherCreateView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def create(self,request,*args,**kwargs):
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save(role='teacher')
            group, created = Group.objects.get_or_create(name=instance.role)
            group.user_set.add(instance)
            return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Request was successful.',
                                 )
        else:
            return send_response(response_code=RESPONSE_CODES['FAILURE'], developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)
                       


# class TeacherListView(generics.ListAPIView):

#     queryset = User.objects.all()
#     serializer_class = UserSignUpSerializer

#     def list(self,request,*args,**kwargs):                  
#         user = User.objects.filter(role='teacher').first()
#         serializer = self.get_serializer(many=True)
#         data = serializer.data
#         return send_response(response_code=RESPONSE_CODES['SUCCESS'], developer_message='Request was successful.',data=data)
