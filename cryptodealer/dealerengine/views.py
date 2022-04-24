from decimal import Decimal
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from authentication import views, urls
from dealerengine.models import Crypto, Membership, Users, Value, History
from django.contrib import messages

'''link to the page with the list of cryptocurrencies'''
class CryptoWeb(LoginRequiredMixin, View):

    def get(self, request):
        """displaying all cryptocurrencies"""
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        values = Value.objects.filter(account=user_id)
        name = Crypto.objects.all()
        context = {
            "name": name,
            "values": values,
            "users": users,
        }
        return render(request, "crypto.html", context=context)


''' page for the list of packages that can be purchased and reduce the purchase commission'''
class MarketWeb(LoginRequiredMixin, View):

    def get(self, request):
        """displaying all packages"""
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        members = Membership.objects.all().order_by('id')
        #######

        context = {
            'user_id': user_id,
            'users': users,
            'members': members,
        }
        return render(request, "market.html", context=context)

    def post(self, request):
        """purchase of the package using the button and assigning it to the current logged-in user"""
        current_user = request.user
        user_id = current_user.id
        member_buy = Users.objects.get(account=user_id)
        members = Membership.objects.all()

        if 'buy0' in request.POST.keys():
            member_buy.member = members[1]
        if 'buy1' in request.POST.keys():
            member_buy.member = members[4]
            member_buy.usd = member_buy.usd - members[4].price
        if 'buy2' in request.POST.keys():
            member_buy.member = members[2]
            member_buy.usd = member_buy.usd - members[2].price
        if 'buy3' in request.POST.keys():
            member_buy.member = members[3]
            member_buy.usd = member_buy.usd - members[3].price
        if 'buy4' in request.POST.keys():
            member_buy.member = members[0]
            member_buy.usd = member_buy.usd - members[0].price
        member_buy.save()

        return redirect('market_view')


""" profile page """
class ProfileWeb(LoginRequiredMixin, View):

    def get(self, request):
        """showing all information about the logged-in user"""
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        ##########
        crypto = Value.objects.filter(account=users).order_by('id')
        crypto_name = Crypto.objects.all()
        value = 1
        context = {
            'users': users,
            'crypto': crypto,
            'crypto_name': crypto_name
        }
        return render(request, "profile.html", context=context)


""" history page """
class HistoryWeb(LoginRequiredMixin, View):
    """showing all transactions made by the logged in user"""

    def get(self, request):
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        histor = History.objects.filter(account=user_id).order_by('date_exchange')
        context = {
            'users': users,
            'histor': histor,
        }
        return render(request, "history.html", context=context)


''' add balance page'''
class BalanceWeb(LoginRequiredMixin, View):
    def get(self, request):
        """showing page"""
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        context = {
            'users': users,
        }
        return render(request, "add_balance.html", context=context)

    def post(self, request):
        """ user can add money to balance account (without add credit card etc.)"""
        current_user = request.user
        user_id = current_user.id
        money = Users.objects.get(account=user_id)
        id_member = money.member.id
        ############################
        if request.POST['cash'] != '':
            take_price = request.POST['cash']
            take_prices = Decimal(take_price)
            if 'buy' in request.POST.keys():
                money.usd = money.usd + take_prices
                t1 = History.objects.create(transaction='buy', name_crypto='Add to wallet'
                                            , value_usd=take_prices)
                t1.account.add(user_id)
            money.save()
        return redirect("add_balance_view")


# ----------------------------------------------------------------------------------------------------------------------


"""Bitcoin page"""
class Bitcoin(LoginRequiredMixin, View):

    def get(self, request):
        """displaying information about bitcoin"""
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        bitcoin = Crypto.objects.filter(pk=1)
        my_value = Value.objects.filter(account=user_id).filter(crypto=1)
        #######
        context = {
            'users': users,
            'bitcoin': bitcoin,
            'my_value': my_value,
        }
        return render(request, "list_crypto/1.html", context=context)

    def post(self, request):
        """buying and selling cryptocurrencies by a logged in user"""
        current_user = request.user
        user_id = current_user.id
        crypto_price = Crypto.objects.get(name="Bitcoin")
        my_value = Value.objects.get(account=user_id, crypto=1)
        money = Users.objects.get(account=user_id)
        id_member = money.member.id
        member_tax = Membership.objects.get(id=id_member)
        ############################
        if request.POST['take_price'] != '':
            take_price = request.POST['take_price']
            take_prices = Decimal(take_price)
            usd_subtraction = crypto_price.price * (take_prices + (take_prices / member_tax.fees))

            if 'buy' in request.POST.keys():
                if money.usd >= (crypto_price.price * take_prices):
                    my_value.value += take_prices
                    money.usd = money.usd - usd_subtraction
                    t1 = History.objects.create(transaction='buy', name_crypto='Bitcoin',
                                                value_crypto=take_prices, value_usd=(usd_subtraction * -1))
                    t1.account.add(user_id)
                else:
                    messages.error(request, "Dont have enough money")
                    return redirect('bitcoin_view')
            if 'sell' in request.POST.keys():
                if my_value.value >= take_prices:
                    my_value.value -= take_prices
                    money.usd = money.usd + (crypto_price.price * take_prices)
                    t1 = History.objects.create(transaction='sell', name_crypto='Bitcoin',
                                                value_crypto=(take_prices * -1), value_usd=usd_subtraction)
                    t1.account.add(user_id)
                else:
                    messages.error(request, "Dont have enough crypto")
                    return redirect('bitcoin_view')
            money.save()
            my_value.save()

        return redirect("bitcoin_view")


"""Litecoin page"""
class Litecoin(LoginRequiredMixin, View):

    def get(self, request):
        """displaying information about litecoin"""
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        litecoin = Crypto.objects.filter(pk=2)
        my_value = Value.objects.filter(account=user_id).filter(crypto=2)
        #######

        context = {
            'users': users,
            'litecoin': litecoin,
            'my_value': my_value,
        }
        return render(request, "list_crypto/2.html", context=context)

    def post(self, request):
        """buying and selling cryptocurrencies by a logged-in user"""
        current_user = request.user
        user_id = current_user.id
        crypto_price = Crypto.objects.get(name="Litecoin")
        my_value = Value.objects.get(account=user_id, crypto=2)
        money = Users.objects.get(account=user_id)
        id_member = money.member.id
        member_tax = Membership.objects.get(id=id_member)
        ############################
        if request.POST['take_price'] != '':
            take_price = request.POST['take_price']
            take_prices = Decimal(take_price)
            usd_subtraction = crypto_price.price * (take_prices + (take_prices / member_tax.fees))
            if 'buy' in request.POST.keys():
                if money.usd >= (crypto_price.price * take_prices):
                    my_value.value += take_prices
                    money.usd = money.usd - usd_subtraction
                    t1 = History.objects.create(transaction='buy', name_crypto='Litecoin',
                                                value_crypto=take_prices, value_usd=(usd_subtraction * -1))
                    t1.account.add(user_id)

                else:
                    messages.error(request, "Dont have enough money")
                    return redirect('litecoin_view')

            if 'sell' in request.POST.keys():
                if my_value.value >= take_prices:
                    my_value.value -= take_prices
                    money.usd = money.usd + (crypto_price.price * take_prices)
                    t1 = History.objects.create(transaction='sell', name_crypto='Litecoin',
                                                value_crypto=(take_prices * -1), value_usd=usd_subtraction)
                    t1.account.add(user_id)
                else:
                    messages.error(request, "Dont have enough crypto")
                    return redirect('litecoin_view')

            money.save()
            my_value.save()

        return redirect("litecoin_view")


"""Dogecoin page"""
class Dogecoin(LoginRequiredMixin, View):

    def get(self, request):
        """displaying information about dogecoin"""
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        dogecoin = Crypto.objects.filter(pk=3)
        my_value = Value.objects.filter(account=user_id).filter(crypto=3)
        #######

        context = {
            'users': users,
            'dogecoin': dogecoin,
            'my_value': my_value,
        }
        return render(request, "list_crypto/3.html", context=context)

    def post(self, request):
        """buying and selling cryptocurrencies by a logged-in user"""
        current_user = request.user
        user_id = current_user.id
        crypto_price = Crypto.objects.get(name="Dogecoin")
        my_value = Value.objects.get(account=user_id, crypto=3)
        money = Users.objects.get(account=user_id)
        id_member = money.member.id
        member_tax = Membership.objects.get(id=id_member)
        ############################
        if request.POST['take_price'] != '':
            take_price = request.POST['take_price']
            take_prices = Decimal(take_price)
            usd_subtraction = crypto_price.price * (take_prices + (take_prices / member_tax.fees))
            if 'buy' in request.POST.keys():
                if money.usd >= (crypto_price.price * take_prices):
                    my_value.value += take_prices
                    money.usd = money.usd - usd_subtraction
                    t1 = History.objects.create(transaction='buy', name_crypto='Dogecoin',
                                                value_crypto=take_prices, value_usd=(usd_subtraction * -1))
                    t1.account.add(user_id)
                else:
                    messages.error(request, "Dont have enough money")
                    return redirect('dogecoin_view')
            if 'sell' in request.POST.keys():
                if my_value.value >= take_prices:
                    my_value.value -= take_prices
                    money.usd = money.usd + (crypto_price.price * take_prices)
                    t1 = History.objects.create(transaction='sell', name_crypto='Dogecoin',
                                                value_crypto=(take_prices * -1), value_usd=usd_subtraction)
                    t1.account.add(user_id)
                else:
                    messages.error(request, "Dont have enough crypto")
                    return redirect('dogecoin_view')
            money.save()
            my_value.save()

        return redirect("dogecoin_view")


"""Tether page"""
class Tether(LoginRequiredMixin, View):

    def get(self, request):
        """displaying information about tether"""
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        tether = Crypto.objects.filter(pk=4)
        my_value = Value.objects.filter(account=user_id).filter(crypto=4)
        #######

        context = {
            'users': users,
            'tether': tether,
            'my_value': my_value,
        }
        return render(request, "list_crypto/4.html", context=context)

    def post(self, request):
        """buying and selling cryptocurrencies by a logged in user"""
        current_user = request.user
        user_id = current_user.id
        crypto_price = Crypto.objects.get(name="Tether")
        my_value = Value.objects.get(account=user_id, crypto=4)
        money = Users.objects.get(account=user_id)
        id_member = money.member.id
        member_tax = Membership.objects.get(id=id_member)
        ############################
        if request.POST['take_price'] != '':
            take_price = request.POST['take_price']
            take_prices = Decimal(take_price)
            usd_subtraction = crypto_price.price * (take_prices + (take_prices / member_tax.fees))
            if 'buy' in request.POST.keys():
                if money.usd >= (crypto_price.price * take_prices):
                    my_value.value += take_prices
                    money.usd = money.usd - usd_subtraction
                    t1 = History.objects.create(transaction='buy', name_crypto='Tether',
                                                value_crypto=take_prices, value_usd=(usd_subtraction * -1))
                    t1.account.add(user_id)
                else:
                    messages.error(request, "Dont have enough money")
                    return redirect('tether_view')
            if 'sell' in request.POST.keys():
                if my_value.value >= take_prices:
                    my_value.value -= take_prices
                    money.usd = money.usd + (crypto_price.price * take_prices)
                    t1 = History.objects.create(transaction='sell', name_crypto='Tether',
                                                value_crypto=(take_prices * -1), value_usd=usd_subtraction)
                    t1.account.add(user_id)
                else:
                    messages.error(request, "Dont have enough crypto")
                    return redirect('tether_view')
            money.save()
            my_value.save()

        return redirect("tether_view")


"""Ethereum page"""
class Ethereum(LoginRequiredMixin, View):
    def get(self, request):
        """displaying information about ethereum"""
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        ethereum = Crypto.objects.filter(pk=5)
        my_value = Value.objects.filter(account=user_id).filter(crypto=5)
        #######

        context = {
            'users': users,
            'ethereum': ethereum,
            'my_value': my_value,
        }
        return render(request, "list_crypto/5.html", context=context)

    def post(self, request):
        """buying and selling cryptocurrencies by a logged-in user"""
        current_user = request.user
        user_id = current_user.id
        crypto_price = Crypto.objects.get(name="Ethereum")
        my_value = Value.objects.get(account=user_id, crypto=5)
        money = Users.objects.get(account=user_id)
        id_member = money.member.id
        member_tax = Membership.objects.get(id=id_member)
        ############################
        if request.POST['take_price'] != '':
            take_price = request.POST['take_price']
            take_prices = Decimal(take_price)
            usd_subtraction = crypto_price.price * (take_prices + (take_prices / member_tax.fees))
            if 'buy' in request.POST.keys():
                if money.usd >= (crypto_price.price * take_prices):
                    my_value.value += take_prices
                    money.usd = money.usd - usd_subtraction
                    t1 = History.objects.create(transaction='buy', name_crypto='Ethereum',
                                                value_crypto=take_prices, value_usd=(usd_subtraction * -1))
                    t1.account.add(user_id)
                else:
                    messages.error(request, "Dont have enough money")
                    return redirect('ethereum_view')
            if 'sell' in request.POST.keys():
                if my_value.value >= take_prices:
                    my_value.value -= take_prices
                    money.usd = money.usd + (crypto_price.price * take_prices)
                    t1 = History.objects.create(transaction='sell', name_crypto='Ethereum',
                                                value_crypto=(take_prices * -1), value_usd=usd_subtraction)
                    t1.account.add(user_id)
                else:
                    messages.error(request, "Dont have enough crypto")
                    return redirect('ethereum_view')
            money.save()
            my_value.save()

        return redirect("ethereum_view")
