def isfloat(socket):
    # this is a renderman node
    if isinstance(socket, dict):
        return socket['renderman_type'] in ['int', 'float']

    elif hasattr(socket.node, 'plugin_name'):
        prop_meta = (
            getattr(socket.node, 'output_meta', [])
            if socket.is_output
            else getattr(socket.node, 'prop_meta', [])
        )
        if socket.name in prop_meta:
            return (
                prop_meta[socket.name]['renderman_type']
                in ['int', 'float']
            )
    else:
        return socket.type in ['INT', 'VALUE']


def isfloat3(socket):
    # this is a renderman node
    if isinstance(socket, dict):
        return socket['renderman_type'] in ['int', 'float']

    elif hasattr(socket.node, 'plugin_name'):
        prop_meta = (
            getattr(socket.node, 'output_meta', [])
            if socket.is_output
            else getattr(socket.node, 'prop_meta', [])
        )
        if socket.name in prop_meta:
            return (
                prop_meta[socket.name]['renderman_type']
                in ['color', 'vector', 'normal']
            )
    else:
        return socket.type in ['RGBA', 'VECTOR']


def samesame(a, b):
    return (
        (type(a) == type(b))
        or
        (isfloat(a) and isfloat(b))
        or
        (isfloat3(a) and isfloat3(b))
    )
