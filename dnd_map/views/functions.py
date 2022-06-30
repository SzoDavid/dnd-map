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
        'depth': item.depth,
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


def calculate_depth(item):
    if item.parent is None:
        return 0
    return calculate_depth(item.parent) + 1


def has_loop(item):
    if item.item_set.count() == 0:
        return False
    checker = 0
    for child in item.item_set.all():
        checker += _has_loop(item, child)
    return checker != 0


def _has_loop(parent, child):
    if parent is child:
        return 1
    if child.item_set.count() == 0:
        return 0
    checker = 0
    for grandchild in child.item_set.all():
        checker += _has_loop(parent, grandchild)
    return checker


def check_leaf_depth(item, item_depth, max_depth):
    return _check_leaf_depth(item, item_depth, max_depth) == 0


def _check_leaf_depth(item, item_depth, max_depth):
    if item_depth > max_depth:
        return 1
    if item.item_set.count() == 0:
        return 0
    checker = 0
    for child in item.item_set.all():
        checker += check_leaf_depth(child, item_depth + 1, max_depth)
    return checker
