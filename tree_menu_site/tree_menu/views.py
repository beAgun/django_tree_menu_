from django.shortcuts import render


# Create your views here.
def index(req):
    return render(req, template_name='tree_menu/index.html', context={'title': 'Главная'})


def show_menu_item(req, menu_item_path):
    data = {
        'title': 'Меню',
        'menu_item_path_selected': menu_item_path,
    }
    return render(req, template_name='tree_menu/index.html', context=data)