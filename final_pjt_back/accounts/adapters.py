from allauth.account.adapter import DefaultAccountAdapter
from .models import CustomUser

class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        user = super().save_user(request, user, form, False)
        
        # Directly assign values to model fields
        user.nickname = request.data.get('nickname', '') 
        user.image = request.data.get('image')
        user.gender = request.data.get('gender')
        user.age = request.data.get('age')
        user.birth = request.data.get('birth')
        user.capital = request.data.get('capital')
        user.salary = request.data.get('salary')
        user.permission = request.data.get('permission',1)
        

        # Set financial_products using the set() method if provided in the request
        financial_products_data = request.data.get('financial_products')
        if financial_products_data:
            financial_products = CustomUser.objects.filter(pk__in=financial_products_data)
            user.financial_products.set(financial_products)

        followings_data = request.data.get('followings')
        if followings_data:
            following_users = CustomUser.objects.filter(pk__in=followings_data)
            user.followings.set(following_users)
        
        user.save()
        return user
