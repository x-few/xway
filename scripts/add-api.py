import os
from jinja2 import Template


def render_file(filename, values):
    with open(filename, 'r') as f:
        template_string = f.read()
    return Template(template_string).render(values)


if __name__ == '__main__':
    table_name = 'permission'

    # TODO: save values, in case we need it in the future.

    values = {
        'table_name': table_name,
        'fields': [
            {'name': 'id', 'type': 'int', 'default': None},
            {'name': 'name', 'type': 'str', 'default': None},
            {'name': 'uri', 'type': 'str', 'default': None},
            {'name': 'description', 'type': 'str', 'default': '""'},
            {'name': 'method', 'type': 'int', 'default': 'PERMISSIONS_METHOD_ALL'},
            {'name': 'status', 'type': 'int',
                'default': 'PERMISSIONS_STATUS_ENABLE',
                'import': 'from utils.const import PERMISSIONS_METHOD_ALL, PERMISSIONS_STATUS_ENABLE'
             },
        ]
    }

    template_files = {
        '../templates/sql.jinja2': '../src/db/queries/sql/{}.sql'.format(table_name),
        '../templates/crud.jinja2': '../src/db/crud/{}.py'.format(table_name),
        '../templates/router.jinja2': '../src/routers/{}.py'.format(table_name),
        '../templates/model.jinja2': '../src/models/{}.py'.format(table_name),
        '../templates/test.jinja2': '../src/tests/{}_test.py'.format(table_name),
    }

    for template_file, res_file in template_files.items():
        print("[+] rendering {} to {}".format(template_file, res_file))
        res = render_file(template_file, values)
        with open(res_file, 'w') as f:
            f.write(res)

        if res_file.endswith(".py"):
            os.system("autopep8 -i {}".format(res_file))
