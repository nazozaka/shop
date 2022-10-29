from django.shortcuts import render, redirect

from . import models

import telebot

bot = telebot.TeleBot('5726564502:AAHmLXaorOwP6vbU1T9XNdbqvV2gMmqzdJM')

def home_page(request):
    all_categories = models.Category.objects.all()

    return render(request, 'index.html', {'all_categories': all_categories})


# Вывести все товары на экран и на front
def get_all_products(request):
    all_products = models.Product.objects.all()# Получить всё
    return render(request, 'index2.html', {'all_products': all_products})


# Получение отдельного товара
def get_exact_product(request, pk):
    current_product = models.Product.objects.get(product_name=pk)

    return render(request, 'exact_product.html', {'current_product': current_product})


def get_exact_category(request, pk):
    current_category = models.Category.objects.get(id=pk)# Получаем данную категорию
    category_products = models.Product.objects.filter(product_category=current_category)# Выводим продукты
    return render(request, 'exact_category.html', {'category_products': category_products})


# Поиск определенного товара
def search_exact_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')
        try:

            models.Product.objects.get(product_name=get_product)

            return redirect(f'/product/{get_product}')

        except:
            return redirect('/')


def add_product_to_user_cart(request, pk):
    if request.method == "POST":
        checker = models.Product.objects.get(id=pk)
        if checker.product_count >= int(request.POST.get('pr_count')):
            models.UserCart.objects.create(user_id=request.user.id,
                                           user_product=checker,
                                           user_product_quantity=int(request.POST.get('pr_count'))).save()

            return redirect('/products')

        else:
            return redirect(f'/product/{checker.product_name}')


def get_exact_user_cart(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    return render(request, 'user_cart.html', {'user_cart': user_cart})


def delete_exact_user_cart(request, pk):
    product_to_delete = models.Product.objects.get(id=pk)
    models.UserCart.objects.filter(user_id=request.user.id,
                                   user_product=product_to_delete).delete()
    return redirect('/user_cart')


def sent_cart_by_bot(request):
    if request.method == "POST":

        user_cart = models.UserCart.objects.filter(user_id=request.user.id)

        message = 'Новый заказ: \n\n'

        for i in user_cart:
            message+=f'{i.user_product} : {i.user_product_quantity} = {i.user_product.product_price*i.user_product_quantity} сум\n'
        bot.send_message(252294897, message)
        models.UserCart.objects.filter(user_id=request.user.id).delete()
        return redirect('/')
