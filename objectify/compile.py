from jinja2 import PackageLoader, Environment
import json


def python_format(value):
    if isinstance(value, (bool, type(None))):
        return str(value)
    else:
        return json.dumps(value)


def python_type(value):
    _type = value['type']
    if _type == 'string':
        return 'str'
    if _type == 'integer':
        return 'int'
    if _type == 'null':
        return 'None'
    if _type == 'number':
        return 'float'
    if _type == 'boolean':
        return 'float'
    if _type == 'array':
        return 'List'  # TODO: item type
    if _type == 'object':
        return value['title']
    raise ValueError('Unknown type: {}'.format(_type))


def py_return_value_start(value):
    _type = value['type']
    if _type == 'object':
        return '{}.create('.format(value['title'])
    else:
        return ''


def py_return_value_end(value):
    _type = value['type']
    if _type == 'object':
        return ')'
    else:
        return ''

env = Environment(loader=PackageLoader(__name__, 'templates'))
env.filters.update({
    'py_primitive': python_format,
    'py_type': python_type,
    'py_return_value_start': py_return_value_start,
    'py_return_value_end': py_return_value_end,
})
template = env.get_template('object.py.tmpl')


schema = {
    "type": "object",
    "title": "Address",
    "properties": {
        "address1": {
            "type": "string"
        },
        "address2": {
            "type": "string"
        },
        "city": {
            "type": "string"
        },
        "country": {
            "type": "string"
        },
        "state": {
            "type": "string",
            "default": "NY"
        },
        "zip": {
            "type": "string"
        },
        "email": {
            "type": "object",
            "title": "Email",
            "properties": {
                "strength": {
                    "type": "number"
                }
            }
        }
    }
}
print '\n\n'.join([
    template.render(**schema),
    template.render(**schema['properties']['email'])
])
