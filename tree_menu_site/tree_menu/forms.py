from django import forms
from django.core.exceptions import ValidationError
from tree_menu.models import Menu


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ('id', 'name', 'slug', 'parent')
        readonly_fields = ('id', )

    @staticmethod
    def get_tree():
        menu = Menu.objects.all()

        tree, roots = {}, []
        for i in menu:
            tree.setdefault(i.id, {'children': []})
            tree[i.id]['name'] = i.name
            tree[i.id]['slug'] = i.slug

            if i.parent_id is None:
                roots += [i.id]
            else:
                tree.setdefault(i.parent_id, {'children': []})
                tree[i.parent_id]['children'] += [i.id]

        def rec(node):
            tree[node]['descendants'] = [node]

            for child in tree[node]['children']:
                tree[node]['descendants'] += rec(child)

            return tree[node]['descendants']

        for root in roots:
            rec(root)
            print('*****tree*****', tree)

        return tree

    def clean(self):
        cleaned_data = super().clean()
        pk, name, parent = self.instance.id, cleaned_data.get('name'), cleaned_data.get('parent')
        tree = self.get_tree()
        if parent is not None:
            if pk in tree:
                if parent.pk in tree[pk]['descendants']:
                    raise ValidationError('Потомок не может быть родителем или '
                                          'нельзя быть родителем для себя самого!')
        super().clean()
