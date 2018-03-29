
_VALID_NODE_STYLE = ['size', 'color', 'shape', 'width',
                     'edgecolor']

_VALID_EDGE_STYLE = ['color', 'width', 'style']

_ALL_STYLE_KEYS = _VALID_NODE_STYLE + _VALID_EDGE_STYLE


def style_merger(*funcs):
    def inner(node_attributes):
        out = {}
        for f in funcs:
            out.update(f(node_attributes))
        return out

    return inner


def use_attributes(keys=None):
    '''Utility style function that searches the given
    attribute dictionary for valid style attributes and bundles
    them into a style dictionary.

    Parameters
    ----------
    keys : str or iterable, optional
        Style keys to search for.

    Returns
    -------
    inner : function
        A style function.
    '''

    def inner(attributes):
        if keys is None:
            return {k: attributes[k] for k in _ALL_STYLE_KEYS \
                    if k in attributes}
        if isinstance(k, str):
            return {keys: attributes[keys]} if keys in attributes else {}
        else:
            return {key: attributes[key] for key in keys \
                    if key in attributes}
    return inner


def apply_style(style, item_iterable):
    styles = {}
    if callable(style):
        for item, item_attr in item_iterable:
            styles[item] = style(item_attr)
    elif isinstance(style, dict):
        for item, item_attr in item_iterable:
            styles[item] = style
    else:
        raise TypeError("style must be dict or callable,"
                        " got {0}".format(type(style)))
    return styles


def generate_node_styles(network, node_style):
    # dict of node id -> node_style_dict
    return apply_style(node_style, network.nodes.data())


def generate_edge_styles(network, edge_style):
    # dict of edge tuple -> edge_style_dict
    return apply_style(edge_style,
                       (((u, v), d) for u, v, d in network.edges.data()))
