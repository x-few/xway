import os
import json
from jinja2 import Template
from datetime import datetime


def render_file(filename, values):
    with open(filename, 'r') as f:
        template_string = f.read()
    return Template(template_string).render(values)


def add_line_to_file(file, add_line, keyword):
    i = 0
    add_line = add_line + '\n'
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if add_line in line:
                print("[!] Warn: {} already exists".format(add_line))
                return

            if keyword in line:
                lines.insert(i, add_line)
                break

            i = i + 1

    with open(file, 'w') as f:
        f.write(''.join(lines))


def under_score_case_2_camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


if __name__ == '__main__':
    # TODO: save values, in case we need it in the future.
    values = {
        'table_name': 'user_role',
        'need_oplog': True,
        'fields': [
            {'name': 'id', 'type': 'int', 'default': None},
            {'name': 'user_id', 'type': 'int', 'default': None},
            {'name': 'role_id', 'type': 'int', 'default': None},
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
        oplog_dep = "Depends(enable_operation_log),"
        add_line_to_file('../src/services/operation_log.py',
                         '    "%s": {"classname": %s, "method": "get_%s_by_id"},' % (
                             values['table_name'],
                             under_score_case_2_camel_case(
                                 values['table_name']),
                             values['table_name']),
                         'auto add map in here')

        add_line_to_file('../src/services/operation_log.py',
                         'from db.crud.{} import {}'.format(
                             values['table_name'],
                             under_score_case_2_camel_case(values['table_name'])),
                         'auto add import in here')

        os.system("autopep8 -i ../src/services/operation_log.py")

    # insert router
    add_line_to_file('../src/routers/__init__.py',
                     'from . import {}'.format(values['table_name']),
                     'add import to here')

    add_line_to_file('../src/routers/__init__.py',
                     '    router.include_router({}.router, prefix="/v1", tags=["{}"],'.format(
                         values['table_name'], values['table_name']),
                     'add router to here')

    add_line_to_file('../src/routers/__init__.py',
                     '                          dependencies=[Depends(get_current_user), {} ],)'.format(
                         oplog_dep),
                     'add router to here')

    os.system("autopep8 -i ../src/routers/__init__.py")
