from pyexpat import model
from rest_framework import serializers
from student_app.models import User, Teacher, Student, Marks, Result

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'email', 'password', 'is_teacher', 'is_student']
        extra_kwargs={
            'id':{'read_only':True},
            'password':{'write_only':True},
        }
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)

# Login Serializer Code Start #
class UserLoginSerializer(serializers.ModelSerializer):
    ''' User Login by email and password '''
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
# Login Serializer Code End #        

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        extra_kwargs={
            'user':{'required':False},
            'fullname':{'required':False},
            'contact':{'required':False},
            'occupation':{'required':False},
            'city':{'required':False}
            
        }
    def create(self, validated_data):
        # validated_data["user"] = self.context["user"]
        return Teacher.objects.create(**validated_data)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs={
            'usersmrk':{'required':False},
        }

    def create(self, validated_data):
         # validated_data["user"] = self.context["user"]
        return Student.objects.create(**validated_data)

class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = "__all__"  

    def create(self, validated_data):
        return Marks.objects.create(**validated_data)    

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"    

    def create(self, validated_data):
        return Result.objects.create(**validated_data)            