def groups_attribute(groups):
    return 'groups="{list}"'.format(list=','.join([i.real_xml_id for i in groups])) if len(groups) else ''


def lst2unicode(lst):
    st = u''
    if isinstance(lst, list) or isinstance(lst, tuple):
        st += '('
        for l in lst:
            if isinstance(l, unicode) or isinstance(l, str):
                st += "u'%s'" % l
                st += ','
            elif isinstance(l, list) or isinstance(l, tuple):
                st += lst2unicode(l)
            else:
                raise
        st += '),'
    return st

def field_options(options):
    opts = []
    for op in options:
        opts.append((op.value, op.name))
    opts = lst2unicode(opts)
    return opts


def field_attrs(field):
    attrs = {}
    if field.required:
        attrs['required'] = field.required_condition and eval(field.required_condition) or True
    if field.invisible:
        attrs['invisible'] = field.invisible_condition and eval(field.invisible_condition) or True
    if field.readonly:
        attrs['readonly'] = field.readonly_condition and eval(field.readonly_condition) or True

    return repr(attrs)
