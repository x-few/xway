import os
import json
from jinja2 import Template
from datetime import datetime


def render_file(filename, values):
    with open(filename, 'r') as f:
        template_string = f.read()
    return Template(template_string).render(values)


def add_line_to_file(file, add_lines, keyword):
    i = 0
    first_line = add_lines[0] + '\n'
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if first_line in line:
                print("[!] Warn: {} already exists".format(first_line))
                return

            if keyword in line:
                # lines.insert(i, first_line)
                for add_line in add_lines:
                    lines.insert(i, add_line + '\n')
                    i = i + 1

                break

            i = i + 1

    with open(file, 'w') as f:
        f.write(''.join(lines))


def under_score_case_2_camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


if __name__ == '__main__':
    # TODO: save values, in case we need it in the future.
    values = {
        'table_name': 'login_log',
        'need_oplog': False,
        'fields': [
            {'name': 'id', 'type': 'int', 'default': None},
            {'name': 'user_id', 'type': 'int', 'default': None},
            {'name': 'host', 'type': 'str', 'default': '""'},
            {'name': 'type', 'type': 'int', 'default': "0"},
            {'name': 'status', 'type': 'int', 'default': None},
        ]
    }

    template_files = {
        '../templates/sql.jinja2': '../src/db/queries/sql/{}.sql'.format(values['table_name']),
        '../templates/crud.jinja2': '../src/db/crud/{}.py'.format(values['table_name']),
        '../templates/router.jinja2': '../src/routers/{}.py'.format(values['table_name']),
        '../templates/model.jinja2': '../src/models/{}.py'.format(values['table_name']),
        '../templates/test.jinja2': '../src/tests/{}_test.py'.format(values['table_name']),
    }

    # render api
    for template_file, res_file in template_files.items():
        print("[+] rendering {} to {}".format(template_file, res_file))
        res = render_file(template_file, values)
        with open(res_file, 'w') as f:
            f.write(res)

        if res_file.endswith(".py"):
            os.system("autopep8 -i {}".format(res_file))

    # backup value
    now = datetime.now()
    values['time'] = now.strftime("%Y-%m-%d-%H%M%S")
    value_file = "../values/{}.json".format(values['table_name'])
    with open(value_file, "w") as f:
        json.dump(values, f, indent=4)

    # insert oplog lines
    oplog_dep = ""
    if values['need_oplog']:
        oplog_dep = "dependencies=[Depends(access_check), Depends(enable_operation_log), ]"
        add_line_to_file('../src/services/operation_log.py',
                         ['    "%s": {"classname": %s, "method": "get_%s_by_id"},' % (
                             values['table_name'],
                             under_score_case_2_camel_case(
                                 values['table_name']),
                             values['table_name']), ],
                         'auto add map in here')

        add_line_to_file('../src/services/operation_log.py',
                         ['from db.crud.{} import {}'.format(
                             values['table_name'],
                             under_score_case_2_camel_case(values['table_name']))],
                         'auto add import in here')

        os.system("autopep8 -i ../src/services/operation_log.py")

    # insert router
    add_line_to_file('../src/routers/__init__.py',
                     ['from . import {}'.format(values['table_name']), ],
                     'add import to here')

    lines = [
        '    router.include_router({}.router,'.format(
            values['table_name']),
        '                          prefix="/v1", tags=["{}"], {},)'.format(
            values['table_name'], oplog_dep),
    ]
    add_line_to_file('../src/routers/__init__.py',
                     lines,
                     'add router to here')

    os.system("autopep8 -i ../src/routers/__init__.py")
