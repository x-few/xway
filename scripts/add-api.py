from jinja2 import Template


def render_file(filename, values):
    with open(filename, 'r') as f:
        template_string = f.read()
    return Template(template_string).render(values)


if __name__ == '__main__':

    # TODO: save values, in case we need it in the future.

    values = {
        'table_name': 'permission',
        'fields': [
            {'name': 'id', 'type': 'int', 'default': None},
            {'name': 'name', 'type': 'str', 'default': None},
            {'name': 'uri', 'type': 'str', 'default': None},
            {'name': 'desc', 'type': 'str', 'default': 'None'},
            {'name': 'method', 'type': 'int', 'default': 'PERMISSIONS_METHOD_ALL'},
            {'name': 'status', 'type': 'int',
                'default': 'PERMISSIONS_STATUS_ENABLE'},
        ]
    }

    res = render_file('../templates/sql.jinja2', values)
    with open('../templates/permission.sql', 'w') as f:
        f.write(res)

    # TODO: reformat python file

    res = render_file('../templates/crud.jinja2', values)
    with open('../templates/permission.crud.py', 'w') as f:
        f.write(res)

    res = render_file('../templates/router.jinja2', values)
    with open('../templates/permission.router.py', 'w') as f:
        f.write(res)

    res = render_file('../templates/model.jinja2', values)
    with open('../templates/permission.model.py', 'w') as f:
        f.write(res)

    res = render_file('../templates/test.jinja2', values)
    with open('../templates/permission_test.py', 'w') as f:
        f.write(res)
