def groups_attribute(groups):
    return 'groups="{list}"'.format(list=','.join([i.real_xml_id for i in groups])) if len(groups) else ''


def field_options(options):
    opts = []
    for op in options:
        opts.append(('u' + op.value.decode("unicode-escape"), 'u' + op.name.decode("unicode-escape")))
    return repr(opts)


def field_attrs(field):
    attrs = {}
    if field.required:
        attrs['required'] = field.required_condition and eval(field.required_condition) or True
    if field.invisible:
        attrs['invisible'] = field.invisible_condition and eval(field.invisible_condition) or True
    if field.readonly:
        attrs['readonly'] = field.readonly_condition and eval(field.readonly_condition) or True

    return repr(attrs)
