from django.urls import reverse


def create_item_node(item, world):
    return {
        'name': str(item.name).replace('\'', '\\u0027'),
        'type': str(item.type).replace('\'', '\\u0027'),
        'details': reverse('dnd_map:details', args=(world.pk, item.pk,)),
        'edit': reverse('dnd_map:edit', args=(world.pk, item.pk,)),
        'discovered': item.discovered,
        'toggle_discovered': reverse('dnd_map:toggle_discovered', args=(world.pk, item.pk,)),
        'description': item.show_description,
        'toggle_description': reverse('dnd_map:toggle_description', args=(world.pk, item.pk,)),
        'add_child': reverse('dnd_map:new', args=(world.pk, item.pk,)),
        'children': [],
        'depth': item.depth,
    }


def create_item_tree(world, item_root, discovered, depth):
    node = create_item_node(item_root, world)

    if depth == 0:
        return node

    if discovered:
        items = item_root.item_set.filter(discovered=True)
    else:
        items = item_root.item_set.all()

    if items.count() == 0:
        return node

    for item in items:
        node['children'].append(create_item_tree(world, item, discovered, depth - 1))

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
        checker += _check_leaf_depth(child, item_depth + 1, max_depth)
    return checker
