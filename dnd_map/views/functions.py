from django.urls import reverse


def create_item_node(item):
    return {
        'name': item.name,
        'details': reverse('dnd_map:details', args=(item.type, item.name)),
        'edit': reverse('dnd_map:edit', args=(item.pk,)),
        'discovered': item.discovered,
        'toggle_discovered': reverse('dnd_map:toggle_discovered', args=(item.pk,)),
        'description': item.show_description,
        'toggle_description': reverse('dnd_map:toggle_description', args=(item.pk,)),
        'add_child': reverse('dnd_map:new', args=(item.pk,)),
        'children': [],
    }


def create_item_tree(item_root, discovered, depth):
    node = create_item_node(item_root)

    if depth == 0:
        return node

    if discovered:
        items = item_root.item_set.filter(discovered=True)
    else:
        items = item_root.item_set.all()

    if items.count() == 0:
        return node

    for item in items:
        node['children'].append(create_item_tree(item, discovered, depth - 1))

    return node
