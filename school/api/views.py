from genericpath import exists
from logging import exception
from tkinter.tix import Tree
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from .decorators import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
# after login user will get access token by JWT 
#POINT 2
class Login(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)
            # email=data.get('email')
            # password=data.get('password')
            if serializer.is_valid():
                username=serializer.data['username']
                password=serializer.data['password']
                user = authenticate(request,username=username, password=password)
                if user is None:
                    return Response({
                        'status':404,
                        'message':'Invalid Password',
                        'data':{}
                    })

                # if user.is_email_verified is False:
                #     return Response({
                #         'status':404,
                #         'message':'Your account is not Verified ',
                #         'data':{}
                #     })


                refresh=RefreshToken.for_user(user)
                users=User.objects.filter(username=username).first()
                return Response({
                    'refresh':str(refresh),
                    'access':str(refresh.access_token),
                    'first_name':users.first_name,
                    'email':users.email,
                    'username':users.username,
                    'is_email_verified':users.is_email_verified


                })


            return Response({
                'status':404,
                'message':'something went wrong',
                'data':serializer.errors
            })


        except Exception as e:
                print(e)
                return Response({
                    'status':404,
                    'error':'something went wrong'
                })



#POINT 1 USER SIGN UP there is a check for password and confirm password 
#so be aware of it and any new user Register will automatically add to student group
class RegisterView(APIView):

    def post(self,request):
        try:
            password =request.data['password']
            confirm_password=request.data['confirm_password']
            if password!=confirm_password:
                return Response({
                    'status':404,
                    'message':'Both Password are Wrong'

                })
            serializer=UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status':403,
                    'errors':serializer.errors

                })
            serializer.save()
            return Response({
                'status':200,
                'message':'Successfully Registered'
            })

        except Exception as e:
            print(e)
            return Response({
                'status':404,
                'error':'something went wrong'
            })

#POINT 6 STUDENT MUST BE ABLE TO SEE HIS INFORMATION ONLY 
#student must have record otherwise it wont show anything
@permission_classes([IsAuthenticated])
class Studentdetail(APIView):
    def get(self,request):
        user=request.user
        try:
            student=StudentRecord.objects.get(user=user)
            serializer=StudentListSerializer(student,many=False)
            return Response({'status':200,
            'data':serializer.data
            ,'message':'successfully retrieved'})
        except Exception as e:
            print(e)
        return Response({
            'message':"Something went wrong"
        })


#ONLY TEACHER AND ADMIN CAN ACCESS THIS URL NOT STUDENTS
#Teacher can watch all students Record in the database
# only those users data who are the members of student group
#POINT 4 Teacher must be able to add/list every user in the database
@permission_classes([IsAuthenticated])
class AllStudentDetails(APIView):
    # @allowed_teachers(allowed_roles=['Teacher'])
    def get(self,request):
        user=request.user
        try:
            if user.groups.filter(name='teacher').exists():

                # student=StudentRecord.objects.all()
                
                studentgroup=User.objects.filter(groups__name__in=['student'])
                print(studentgroup)
                # .values_list('pk',flat=True)
                # print(list(studentgroup))
                # studentgroup=list(studentgroup)


                # student=StudentRecord.objects.filter(user__id__in=studentgroup)
                # print(student)
                serializer=UserdetailSerializer(studentgroup,many=True)
                return Response({'status':200,
                'data':serializer.data
                ,'message':'successfully All Data Retrieved'})
            return Response({'status':200,
                'message':'You are not authorised'})
        except Exception as e:
            print(e)
        return Response({
            'message':"Something went wrong "
        })

#this action is for superadmin who can add user in any group
# like teacher,student etc
#POINT 5 admin must be able to add/list every user in the database
@permission_classes([IsAuthenticated])
class AddStudent(APIView):
    def post(self,request):
        user=request.user
        try:
            if user.groups.filter(name='super-admin').exists():
                username=request.data['username']
                group=request.data['group']
                user=User.objects.filter(username=username).first()
                group=Group.objects.filter(name=group).first()
                if user.groups.filter(name=group):
                    return Response({
                        'message':f"{user} is already added to the {group} Group"
                    })
                if user and group :
                    group.user_set.add(user)
                    return Response({
                        'message':f"{user.username} is added to the {group} Group "
                    })
                return Response({
                    'message':'Invalid Data'

                })
            return Response({
                    'message':'You are not authorised for this action '

                })
        except Exception as e:
            print(e)
        return Response({
            'message':"oops ! Something went wrong"
        })


#POINT 5 Part 2 admin can list evry user in the database with thier 
# group names 
@permission_classes([IsAuthenticated])
class listallusers(APIView):
    def get(self,request):
        user=request.user
        try:
            if user.groups.filter(name='super-admin').exists():
                student=User.objects.all()
                serializer=UserSerializer(student,many=True)

                return Response({'status':200,
                'data':serializer.data
                ,'message':'successfully All Data Retrieved'})
            return Response({'status':200,
                'message':'You are not authorised'})
        except Exception as e:
            print(e)
        return Response({
            'message':"Something went wrong "
        })






#POINT 4 Teacher must be able to add/list the user into students group
# Teacher can't add user to other groups like teacher and super-admin groups
@permission_classes([IsAuthenticated])
class AddStudentbyTeacher(APIView):
    def post(self,request):
        user=request.user
        try:
            if user.groups.filter(name='teacher').exists():
                print(user.groups.all())
                username=request.data['username']
                group=request.data['group']
                user=User.objects.filter(username=username).first()
                group=Group.objects.filter(name=group).first()
                if user.groups.filter(name=group):
                    return Response({
                        'message':f"{user} is already added to the {group} Group"
                    })
                # if group !='student':
                #     return Response({
                #         'message':"You are not authorised for this action"
                #     })
                if user and group :
                    if group !='student':#teacher can only add users to student group not others group
                        return Response({
                            'message':"You are not authorised for this action"
                        })
                    group.user_set.add(user)
                    return Response({
                        'message':f"{user.username} is added to the {group} Group "
                    })
                return Response({
                    'message':'Invalid Data'

                })
            return Response({
                    'message':'You are not authorised for this action '

                })
        except Exception as e:
            print(e)
        return Response({
            'message':"oops ! Something went wrong"
        })



                    




