from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from ..models import Menu

register = template.Library()


@register.inclusion_tag('tree_menu/tree_menu2.html', takes_context=True)
def draw_menu(context, menu_name):
    path_lst = context['request'].path.split('/')
    while '' in path_lst:
        path_lst.remove('')

    menu = Menu.objects.all()

    tree, root = {}, None
    for i in menu:
        tree.setdefault(i.id, {'children': []})
        tree[i.id]['name'] = i.name
        tree[i.id]['slug'] = i.slug

        if i.name == menu_name:
            root = i.id
        elif i.parent_id is not None:
            tree.setdefault(i.parent_id, {'children': []})
            tree[i.parent_id]['children'] += [i.id]

    def rec(node, tree):
        if node == root:
            tree[node]['path'] = reverse('menu_item',
                                         kwargs={'menu_item_path': tree[node]['slug']})

        for child in tree[node]['children']:
            tree[child]['path'] = tree[node]['path'] + tree[child]['slug'] + '/'
            tree = rec(child, tree)

        return tree

    if root:
        tree = rec(root, tree)

        return {'path_lst': path_lst, 'node': tree[root], 'tree': tree,}