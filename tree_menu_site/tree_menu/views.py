from django.shortcuts import render


def index(req):
    data = {
        'title': 'Главная',
    }
    return render(req, template_name='tree_menu/index.html', context=data)


def show_menu_item(req, menu_item_path):
    data = {
        'title': 'Меню',
    }
    return render(req, template_name='tree_menu/index.html', context=data)
