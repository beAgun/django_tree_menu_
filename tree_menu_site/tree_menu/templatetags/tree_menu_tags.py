from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from ..models import Menu

register = template.Library()


@register.inclusion_tag('tree_menu/menu_root.html', takes_context=True)
def draw_menu(context, menu_name):
    path_lst = ['']
    if 'menu_item_path_selected' in context:
        path_lst = context['menu_item_path_selected'].split('/')
    menu = Menu.objects.all()

    tree = {}
    for i in menu:
        tree[i.id] = {'name': i.name, 'slug': i.slug, 'children': []}

        if i.parent_id is None:
            if i.name == menu_name:
                root = i.id
        else:
            tree[i.parent_id]['children'] += [i.id]

    def rec(node, tree):
        if node == root:
            tree[node]['path'] = reverse('menu_item',
                                         kwargs={'menu_item_path': tree[node]['slug']})

        for child in tree[node]['children']:
            tree[child]['path'] = tree[node]['path'] + tree[child]['slug'] + '/'
            tree = rec(child, tree)

        return tree

    tree = rec(root, tree)

    return {'path_lst': path_lst, 'node': tree[root], 'children': tree[root]['children'], 'tree': tree}
