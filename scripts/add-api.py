import os
import json
from jinja2 import Template
from datetime import datetime


def render_file(filename, values):
    with open(filename, 'r') as f:
        template_string = f.read()
    return Template(template_string).render(values)


if __name__ == '__main__':
    # TODO: save values, in case we need it in the future.
    values = {
        'table_name': 'role',
        'fields': [
            {'name': 'id', 'type': 'int', 'default': None},
            {'name': 'name', 'type': 'str', 'default': None},
            {'name': 'description', 'type': 'str', 'default': '""'},
        ]
    }

    template_files = {
        '../templates/sql.jinja2': '../src/db/queries/sql/{}.sql'.format(values['table_name']),
        '../templates/crud.jinja2': '../src/db/crud/{}.py'.format(values['table_name']),
        '../templates/router.jinja2': '../src/routers/{}.py'.format(values['table_name']),
        '../templates/model.jinja2': '../src/models/{}.py'.format(values['table_name']),
        '../templates/test.jinja2': '../src/tests/{}_test.py'.format(values['table_name']),
    }

    for template_file, res_file in template_files.items():
        print("[+] rendering {} to {}".format(template_file, res_file))
        res = render_file(template_file, values)
        with open(res_file, 'w') as f:
            f.write(res)

        if res_file.endswith(".py"):
            os.system("autopep8 -i {}".format(res_file))

    now = datetime.now()
    values['time'] = now.strftime("%Y-%m-%d-%H%M%S")

    value_file = "../values/{}.json".format(values['table_name'])

    with open(value_file, "w") as f:
        json.dump(values, f, indent=4)
