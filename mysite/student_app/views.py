
from .models import Marks, Teacher, User, Student, Result
from student_app.serializers import UserRegisterSerializer, TeacherSerializer, StudentSerializer, UserLoginSerializer, MarksSerializer, ResultSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
import json
# Create your views here.

# Generate Manual Token Code Start #
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      
  }


class UserRegistrationView(APIView):
    # renderer_classes = [UserRenderer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self, request, format=None):
        print(request.data)    
        register_dict = {}
        email = request.data.pop("email")
        password = make_password(request.data.pop("password"))
        print(password)
        if "occupation" in request.data:
            print("A")
            register_dict = {
                "email":email,
                "password":password,
                "is_teacher":True,
                "is_student":False
            }
        else:
            print("B")
            register_dict = {
                "email":email,
                "password":password,
                "is_teacher":False,
                "is_student":True
            }
        serializer = UserRegisterSerializer(data=register_dict)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            token = get_tokens_for_user(user)
            print(token,"token 2")
            user_id = serializer.data.get("id")# 25
            print(user_id)
            firstname = request.data.pop("firstname")
            lastname = request.data.pop("lastname")
            request.data["fullname"] = firstname + " " + lastname
            request.data["user"] = user_id
            
            if "occupation" in request.data:
                teacher = TeacherSerializer(data=request.data)
                if teacher.is_valid(raise_exception=False):
                    teacher.save()
                else:
                    return Response({"message":"teacher data not saved"})
            else:
                student = StudentSerializer(data=request.data)
                if student.is_valid(raise_exception=False):
                    student.save()
                else:
                    print(student.errors)
                    return Response({"message":"student data not saved"})
            data_dict = {}
            if "occupation" in request.data:
                data_dict = {
                    "user":serializer.data,
                    "teacher":teacher.data,
                    'access_token':token.get('access'),
                    'refresh_token':token.get('refresh')
                }
            else:
                data_dict = {
                    "user":serializer.data,
                    "student":student.data,
                    'access_token':token.get('access'),
                    'refresh_token':token.get('refresh')
                }
            return Response({"data":data_dict})
        else:

            return Response({"message":serializer.errors})

# User Login Api Code Start #
class LoginView(APIView):
    # renderer_classes = [UserRenderer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                try:
                    user = User.objects.get(email=serializer.data.get('email'))
                except User.DoesNotExist:
                    return Response({"status":"false", "message":"User Detail Not Found"}, status=status.HTTP_404_NOT_FOUND)

                User_data = {
                    'email':user.email,
                    'access_token':token.get('access'),
                    'refresh_token':token.get('refresh')
                }
                return Response({"status":True, "message":"Login Successfully", "data":User_data}, status=status.HTTP_200_OK)
            else:
                return Response({"status":"false", "message":{"non_field_errors":["Email or Password is not valid"]}}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status":"false", "message":"Some Fields Are Missing"}, status=status.HTTP_400_BAD_REQUEST)
# User Login Api Code End #

class TeacherView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
             return Response({"status":"false","message": "The data does not exist"}, status=status.HTTP_404_NOT_FOUND)

        
    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        

        # income = self.get_object(id=pk, user_id=str(user.id))
        try:
            teacher = Teacher.objects.get(id=pk, user_id=user)
        except:
            return Response({'status':False, 'message':'teacher data not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)


    def put(self,request,pk,format=None):
        if "user" in request.data and request.data['user'] != "":
           return Response({'status':False, 'message':'user cannot modifay'}, status=status.HTTP_404_NOT_FOUND) 
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            teacher = Teacher.objects.get(id=pk, user_id=user)
        except:
            return Response({'status':False, 'message':'teacher data not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherSerializer(teacher,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True, "message":"update data Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
      
# User goal API Code End # 


class StudentView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
             return Response({"status":"false","message": "The data does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(email=request.user).id
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            student = Student.objects.get(id=pk, user_id=user)
        except:
            return Response({'status':False, 'message':'Student data not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherSerializer(student)
        return Response(serializer.data)

class MarksCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk=None):
        try:
            user = User.objects.get(email=request.user)
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            student = Student.objects.get(id=pk)
        except:
            return Response({'status':False, 'message':'student data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_teacher:
            request.data["usersmrk"] = student.id
            request.data["userstd"] = None
            serializer = MarksSerializer(data=request.data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                is_pass = False
                subject1=int(serializer.data.get("subject1"))
                subject2=int(serializer.data.get("subject2"))
                subject3=int(serializer.data.get("subject3"))
                subject4=int(serializer.data.get("subject4"))
                subject5=int(serializer.data.get("subject5"))

                if subject1 < 30 or subject2 < 30 or subject3 < 30 or subject4 < 30 or subject5 < 30:
                    is_pass = False
                else:
                    is_pass = True

                sum = subject1+subject2+subject3+subject4+subject5
                percentage = sum/5 
                result_dict = {
                    "total":sum,
                    "percentage":percentage,
                    "is_pass":str(is_pass)
                }
                result = ResultSerializer(data=result_dict)
                if result.is_valid(raise_exception=False):
                    result.save() 
                    Marks.objects.filter(id=serializer.data.get("id")).update(userstd_id=result.data.get("id"))  
                    mark_dict = {
                        "id":serializer.data.get("id"),
                        "subject1":serializer.data.get("subject1"),
                        "subject2":serializer.data.get("subject2"),
                        "subject3":serializer.data.get("subject3"),
                        "subject4":serializer.data.get("subject4"),
                        "subject5":serializer.data.get("subject5"),
                        "usersmrk":serializer.data.get("usersmrk"),
                        "userstd":result.data.get("id")
                    }
                    data_dict = {
                        "mark":mark_dict,
                        "result":result.data
                    }

                    ####### custom dict######
                    # data_dict = {
                    #     "subject1":serializer.data.get("subject1"),
                    #     "subject2":serializer.data.get("subject2"),
                    #     "subject3":serializer.data.get("subject3"),
                    #     "subject4":serializer.data.get("subject4"),
                    #     "subject5":serializer.data.get("subject5"),
                    #     "total":result.data.get("total"),
                    #     "is_pass":result.data.get("is_pass"),
                    #     "percentage":result.data.get("percentage")
                    # }
                    return Response({"status":True, "data":data_dict}, status=status.HTTP_201_CREATED)
                else:
                    print(result.errors)
                    return Response({"message":"result data not saved"})    
                    
            else:
                return Response({"status":"unsuccess"})

        else:
            return Response({'status':False, 'message':'student cannot add Mask'}, status=status.HTTP_400_BAD_REQUEST) 
            
    def get(self, request, pk=None):
        print(request.user.is_teacher)
        data_dict = {}
        data_list = []

        if pk is None:
            try:
                user = User.objects.get(email=request.user)
            except User.DoesNotExist:
                return Response({"message":"error1"})

            if user.is_teacher:
                students = Student.objects.all()
                for x in students:
                    try:
                        marks = Marks.objects.get(usersmrk=str(x.id))
                        marks = MarksSerializer(marks, many=False)
                        marks = marks.data
                    except Marks.DoesNotExist:
                        marks = {}
                    
                    if marks != {}:
                        try:
                            result = Result.objects.get(id=str(marks.get("userstd")))
                            result = ResultSerializer(result, many=False)
                            result = result.data
                        except Result.DoesNotExist:
                            pass
                    else:
                        result = {}
                    
                    
                    data = {
                        "fullname":x.fullname,
                        "contact":x.contact,
                        "student_class":x.student_class,
                        "city":x.city,
                        "marks":marks,
                        "result":result
                    }
                    data_list.append(data)
                data_dict["students"] = data_list
            else:
                student = Student.objects.get(user=user.id)
                marks = Marks.objects.filter(usersmrk=student.id)
                marks = MarksSerializer(marks, many=True)
                result = Result.objects.filter(id=marks.data[0]["userstd"])
                result = ResultSerializer(result, many=True)
                data_dict["Mark Data"] = {
                    "student":{
                        "fullname":student.fullname,
                        "contact":student.contact,
                        "student_class":student.student_class,
                        "city":student.city,
                        "marks":marks.data,
                        # "result":str(result)
                        "result":result.data
                    }
                }
            return Response({"data":data_dict})
        else:
            try:
                user = User.objects.get(email=request.user)
            except User.DoesNotExist:
                return Response({"message":"error1"})
            if user.is_teacher:
                student = Student.objects.get(id=pk)
                marks = Marks.objects.filter(usersmrk=student.id)
                marks = MarksSerializer(marks, many=True)
                print(marks.data)
                result = Result.objects.filter(id=marks.data[0]["userstd"])
                print(result)
                result = ResultSerializer(result, many=True)
                data_dict["Mark Data"] = {
                    "student":{
                        "fullname":student.fullname,
                        "contact":student.contact,
                        "student_class":student.student_class,
                        "city":student.city,
                        "marks":marks.data,
                        "result":result.data
                    }
                }
            else:
                return Response({"message":"error2"})
            return Response({"data":data_dict})
    def put(self,request,pk,format=None):
        try:
            user = User.objects.get(email=request.user) 
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            student = Student.objects.get(id=pk)
        except:
            return Response({'status':False, 'message':'student data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_teacher:
            request.data["usersmrk"] = student.id
            try:
                marks = Marks.objects.get(usersmrk_id=student, id=request.data.get('id'))
            except Marks.DoesNotExist:
                return Response({'status':False, 'message':'marks data not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = MarksSerializer(marks,data=request.data)
            if serializer.is_valid():
                serializer.save()
                is_pass = False
                subject1=int(serializer.data.get("subject1"))
                subject2=int(serializer.data.get("subject2"))
                subject3=int(serializer.data.get("subject3"))
                subject4=int(serializer.data.get("subject4"))
                subject5=int(serializer.data.get("subject5"))
        
                if subject1 < 30 or subject2 < 30 or subject3 < 30 or subject4 < 30 or subject5 < 30:
                    is_pass = False
                else:
                    is_pass = True

                sum = subject1+subject2+subject3+subject4+subject5
                percentage = sum/5 
                result_dict = {
                    "userstd":student.id,
                    "total":sum,
                    "percentage":percentage,
                    "is_pass":str(is_pass)
                }
                try:
                    resultup = Result.objects.get(userstd_result=marks, id=request.data.get('result_id'))
                except Result.DoesNotExist:
                    return Response({'status':False, 'message':'result data not found'}, status=status.HTTP_404_NOT_FOUND)   
                result = ResultSerializer(resultup,data=result_dict)
                if result.is_valid(raise_exception=False):
                    result.save()   
                    data_dict = {
                        "mark":serializer.data,
                        "result":result.data
                    }
    
                
                return Response({"status":True, "message":"update data Successfully", "data":data_dict}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({"status":False})    
    def delete(self,request,pk):
        try:
            user = User.objects.get(email=request.user) 
        except User.DoesNotExist:
            return Response({'status':False, 'message':'user data not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            student = Student.objects.get(id=pk)
        except:
            return Response({'status':False, 'message':'student data not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_teacher:
            request.data['usersmrk']=student.id
            # mark table get result id 
            # result filter 
            result_id = Marks.objects.get(usersmrk=student.id)
            print(result_id)
            if result_id:
                Result.objects.filter(userstd_result=result_id).delete()
            student.delete()
            return Response({"status":True,"message":"Data was successfully delete"}, status=status.HTTP_200_OK)
        else:
            return Response({'status':False, 'message':'Data was unsuccessfully delete'}, status=status.HTTP_404_NOT_FOUND)        
