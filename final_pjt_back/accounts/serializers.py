from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'nickname']  # 'nickname' 필드가 유저 모델에 있는지 확인


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=100)
    gender = serializers.ChoiceField(choices=CustomUser.GENDER_CHOICES)
    birth = serializers.DateField(format="%Y-%m-%d")  # 생년월일 필드
    capital = serializers.IntegerField(default=0, required=False)
    salary = serializers.IntegerField(default=0, required=False)

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
        user.save()
        return user
