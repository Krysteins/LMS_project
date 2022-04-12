from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from authentication import views
from dealerengine.models import Crypto, Membership, Users, Value


class CryptoWeb(View):
    def get(self, request):
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        values = Value.objects.filter(account=user_id)
        name = Crypto.objects.all()
        loged = User
        context = {
            "name": name,
            "values": values,
            "users": users,
        }
        return render(request, "crypto.html", context=context)


class MarketWeb(View):
    def get(self, request):
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        #######
        members = Membership.objects.all().order_by('id')
        #######

        context = {
            'user_id': user_id,
            'users': users,
            'members': members,
        }
        return render(request, "market.html", context=context)

    def post(self, request):
        current_user = request.user
        user_id = current_user.id
        member_buy = Users.objects.filter(pk=user_id)
        if 'buying0' in request.POST.keys() and request.POST['buying0']:
            member_buy.member = 0
        if 'buying1' in request.POST.keys() and request.POST['buying1']:
            member_buy.member = 1
        if 'buying2' in request.POST.keys() and request.POST['buying2']:
            member_buy.member = 2
        if 'buying3' in request.POST.keys() and request.POST['buying3']:
            member_buy.member = 3
        if 'buying4' in request.POST.keys() and request.POST['buying4']:
            member_buy.member = 4
        for objects in member_buy:
            objects.save()

        return redirect('market_view')


class ProfileWeb(View):
    def get(self, request):
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        context = {
            'users': users
        }
        return render(request, "profile.html", context=context)

# class(View):
#     def get(self, request):
#         context = {
#
#         }
#         return render(request, "crypto.html", context=context)
#
#
# class(View):
#     def get(self, request):
#         context = {
#
#         }
#         return render(request, "crypto.html", context=context)
#
#
# class(View):
#     def get(self, request):
#         context = {
#
#         }
#         return render(request, "crypto.html", context=context)

#
# class(View):
#     def get(self, request):
#         context = {
#
#         }
#         return render(request, "crypto.html", context=context)
