from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from dj_rest_auth.serializers import JWTSerializer as DefaultJWTSerializer
from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class CustomTokenSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    nickname= serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    id =  serializers.SerializerMethodField()
    def get_username(self, obj):
        return obj.user.username

    def get_nickname(self,obj):
        return obj.user.nickname
    
    def get_email(self,obj):
        return obj.user.email
    
    def get_id(self,obj):
        return obj.user.id
    class Meta:
        model = Token
        fields = ('key', 'user', 'username','nickname','email','id')


class CustomLoginSerializer(DefaultLoginSerializer):
    def get_response_data(self, user):
        data = super().get_response_data(user)
        data['username'] = user.username  # 사용자 이름 추가
        #data['nickname'] = user.nickname
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        #fields = ['username', 'nickname','email','followings']  # 'nickname' 필드가 유저 모델에 있는지 확인
        exclude = ('password',)

class CustomUserDetailSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'image', 'nickname', 'gender',
            'birth', 'capital', 'salary',
            'created_at', 'updated_at', 'followings', 'followers','id'
        ]
        depth = 1  # followings 필드를 위한 설정

    def get_followers(self, obj):
        # obj는 User 모델의 인스턴스
        return [follower.username for follower in obj.followers.all()]

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=100)
    gender = serializers.ChoiceField(choices=CustomUser.GENDER_CHOICES)
    birth = serializers.DateField(format="%Y-%m-%d")  # 생년월일 필드
    capital = serializers.IntegerField(default=0, required=False)
    salary = serializers.IntegerField(default=0, required=False)

    def validate_nickname(self, value):
        if CustomUser.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def get_cleaned_data(self):
        print(self.validated_data)
        data = super().get_cleaned_data()
        data.update({
            'nickname': self.validated_data.get('nickname', ''),
            'gender': self.validated_data.get('gender', ''),
            'birth': self.validated_data.get('birth', '2023-11-11'),  # 기본값을 None으로 설정
            'capital': self.validated_data.get('capital', 0),
            'salary': self.validated_data.get('salary', 0)
        })
        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.cleaned_data.get('nickname')
        user.gender = self.cleaned_data.get('gender')
        user.birth = self.cleaned_data.get('birth')
        user.capital = self.cleaned_data.get('capital')
        user.salary = self.cleaned_data.get('salary')
        user.email = self.cleaned_data.get('email')
        user.save()
        return user
