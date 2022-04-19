from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from authentication import views
from dealerengine.models import Crypto, Membership, Users, Value, History
from django.contrib import messages


# odnośnik do strony z listą kryptowalut
class CryptoWeb(View):
    def get(self, request):
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


# odnośnik do strony z listą pakietów, które zmniejszają prowizję zakupu
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
        member_buy = Users.objects.get(account=user_id)
        members = Membership.objects.all()
        money = Users.objects.get(account=user_id)
        if 'buy0' in request.POST.keys():
            member_buy.member = members[4]
        if 'buy1' in request.POST.keys():
            member_buy.member = members[0]
            money.usd = money.usd - members[0].price
        if 'buy2' in request.POST.keys():
            member_buy.member = members[1]
            money.usd = money.usd - members[1].price
        if 'buy3' in request.POST.keys():
            member_buy.member = members[2]
            money.usd = money.usd - members[2].price
        if 'buy4' in request.POST.keys():
            member_buy.member = members[3]
            money.usd = money.usd - members[3].price
        member_buy.save()
        money.save()

        return redirect('market_view')


class ProfileWeb(View):
    def get(self, request):
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        ##########
        crypto = Value.objects.filter(account=user_id).order_by('id')
        crypto_name = Crypto.objects.all()
        value = 1
        context = {
            'users': users,
            'crypto': crypto,
            'crypto_name': crypto_name
        }
        return render(request, "profile.html", context=context)


class HistoryWeb(View):
    def get(self, request):
        current_user = request.user
        user_id = current_user.id
        users = Users.objects.filter(account=user_id)
        histor = History.objects.filter(account=user_id).order_by('date_exchange')
        context = {
            'users': users,
            'histor:': histor,
        }
        return render(request, "history.html", context=context)


###################################################################################################################
# klasa poświęcona Bitcoin'em
class Bitcoin(View):
    # wyświetlanie informacji do strony z bitcoin'em
    def get(self, request):
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
    # pobieranie informacji zakupu lub sprzedaży kryptowaluty oraz wprowadzanie ich do bazy danych
    def post(self, request):
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


class Litecoin(View):
    def get(self, request):
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


class Dogecoin(View):
    def get(self, request):
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


class Tether(View):
    def get(self, request):
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


class Ethereum(View):
    def get(self, request):
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
