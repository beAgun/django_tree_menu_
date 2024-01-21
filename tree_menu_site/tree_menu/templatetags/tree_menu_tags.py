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

#----------------------------------------------------------------------------------------------------------
# другие способы
@register.simple_tag(takes_context=True)
def draw_menu2(context, menu_name):
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

    def rec(root, tree, url, temp):
        temp += '<ul>'
        for child in tree[root]['children']:
            child_url = url + tree[child]['slug'] + '/'

            temp += f'<li><a href="{child_url}">{tree[child]["name"]}</a>'

            if tree[child]['slug'] in path_lst:
                temp = rec(child, tree, child_url, temp)
            temp += '</li>'
        temp += '</ul>'

        return temp

    url = reverse('menu_item', kwargs={'menu_item_path': tree[root]['slug']})
    temp = rec(root, tree, url, f'<ul><li><a href="{url}">{tree[root]["name"]}</a>') + '</ul>'

    return mark_safe(temp)


    # query = '''
    #     with recursive m(path, id, parent_id, slug, name) as (
    #     select slug path, id, parent_id, slug, name
    #     from tree_menu_menu
    #     where name = %s and parent_id is null
    #     union all
    #     select path || '/' || t.slug, t.id, t.parent_id, t.slug, t.name
    #     from tree_menu_menu  t, m
    #     where t.parent_id = m.id
    #     )
    #     select * from m
    #     order by id;
    # '''
    # menu = Menu.objects.raw(query, [menu_name])


# @register.simple_tag(takes_context=True)
# def draw_menu3(context, menu_name):
#     query = '''
#         with recursive r
#         as (select id, name, 1 as lvl, parent_id
#             from tree_menu_menu as t
#             where name = %s
#             UNION ALL
#             select m.id, m.name, lvl + 1, m.parent_id
#             from tree_menu_menu m
#             join r
#             on m.parent_id = r.id
#         )
#         select id, name, lvl, parent_id
#         from r
#         ;
#     '''
#     menu = Menu.objects.raw(query, [menu_name])
#     return {'menu': menu, 'menu_name': menu_name}