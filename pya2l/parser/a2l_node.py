"""
@project: pya2l
@file: a2l_node.py
@author: Guillaume Sottas
@date: 05.04.2018
"""

from pya2l.parser.node import ASTNode, node_type
from pya2l.parser.a2l_type import *

enum_index_mode = Ident
enum_attribute = Ident
enum_type = Ident
enum_conversion_type = Ident
enum_prg_type = Ident
enum_memory_type = Ident
enum_mode = Ident
monotony_enum = Ident
enum_tag = Ident


class A2lNode(ASTNode):
    def __setattr__(self, key, value):
        if hasattr(self, key) and isinstance(getattr(self, key), String):
            value = String(value)
        return super(A2lNode, self).__setattr__(key, value)

    def dump(self, n=0):
        p, k = self.positionals(), self.keywords()
        if len(k) and len(p):
            yield n, '/begin {} {}'.format(self.node, ' '.join('{}' for _ in p)).format(*[next(x)[1] for x in [e.dump() for e in p]]).rstrip()
        elif len(k):
            yield n, '/begin {}'.format(self.node)
        else:
            yield n, '{} {}'.format(self.node, ' '.join('{}' for _ in p)).format(*[next(x)[1] for x in [e.dump() for e in p]]).rstrip()
        for o in filter(lambda x: x not in (None, dict()), k):
            for e in o.dump(n=n+1):
                yield e
        if len(k):
            yield n, '/end {}'.format(self.node)


class A2lTagNode(A2lNode):
    def dump(self, n=0):
        yield n, '{node} {value}'.format(node=self.node, value=getattr(self, list(self.properties)[0]))


@node_type('a2l')
class A2lFile(A2lNode):
    __slots__ = 'asap2_version', 'a2ml_version', 'project'

    def __init__(self, args):
        self.asap2_version = None
        self.a2ml_version = None
        self.project = None
        super(A2lFile, self).__init__(*args)

    def dump(self, n=0):
        for p in (getattr(self, p) for p in self.properties):
            if p is not None:
                for e in p.dump(n=0):
                    yield e


@node_type('IF_DATA')
class IF_DATA(A2lNode):
    def __new__(cls, tag=None, value=None):
        cls.__slots__ = cls.__slots__ + tuple([tag])
        setattr(cls, tag, value)
        return super(IF_DATA, cls).__new__(cls)

    def __init__(self, tag=None, value=None):
        super(IF_DATA, self).__init__((tag, value))

    def dict(self):
        return dict((tag, getattr(self, tag).dict()) for tag in self.properties)

    def dump(self, n=0):
        for tag, value in ((t, getattr(self, t)) for t in self.properties):
            yield n, '/begin {node} {tag}'.format(node=self.node, tag=tag)
            for e in value.dump(n=n + 1):
                yield e
            yield n, '/end {node}'.format(node=self.node)


@node_type('A2ML')
class A2ML(A2lNode):
    def __new__(cls, a2ml):
        cls.__slots__ = tuple(['type_definition'] + list(b.tag for b in filter(lambda d: hasattr(d, 'tag'), a2ml)))
        setattr(cls, 'type_definition', list())
        for e in a2ml:
            if hasattr(e, 'tag'):
                setattr(cls, e.tag, e)
            # elif e not in getattr(cls, 'type_definition'):
            #     getattr(cls, 'type_definition').append(e)
        return super(A2ML, cls).__new__(cls)

    def __init__(self, a2ml):
        args = [('type_definition', d) for d in filter(lambda d: not hasattr(d, 'tag'), a2ml)]
        for block in filter(lambda d: hasattr(d, 'tag'), a2ml):
            args.append((block.tag, block))
        super(A2ML, self).__init__(*args)

    def dump(self, n=0):
        return (e for e in super(A2ML, self).dump(n=n))


@node_type('A2ML_VERSION')
class A2ML_VERSION(A2lNode):
    __slots__ = 'version_no', 'upgrade_no', 

    def __init__(self, version_no, upgrade_no, ):
        self.version_no = Int(version_no)
        self.upgrade_no = Int(upgrade_no)
        super(A2ML_VERSION, self).__init__()

    def positionals(self):
        return [e for e in (self.version_no,
                            self.upgrade_no,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('ADDR_EPK')
class ADDR_EPK(Long):
    def __init__(self, address):
        super(ADDR_EPK, self).__init__(self, address)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ADDR_EPK, self).dump())[1])


@node_type('ALIGNMENT_BYTE')
class ALIGNMENT_BYTE(Int):
    def __init__(self, alignment_border):
        super(ALIGNMENT_BYTE, self).__init__(self, alignment_border)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ALIGNMENT_BYTE, self).dump())[1])


@node_type('ALIGNMENT_FLOAT32_IEEE')
class ALIGNMENT_FLOAT32_IEEE(Int):
    def __init__(self, alignment_border):
        super(ALIGNMENT_FLOAT32_IEEE, self).__init__(self, alignment_border)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ALIGNMENT_FLOAT32_IEEE, self).dump())[1])


@node_type('ALIGNMENT_FLOAT64_IEEE')
class ALIGNMENT_FLOAT64_IEEE(Int):
    def __init__(self, alignment_border):
        super(ALIGNMENT_FLOAT64_IEEE, self).__init__(self, alignment_border)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ALIGNMENT_FLOAT64_IEEE, self).dump())[1])


@node_type('ALIGNMENT_LONG')
class ALIGNMENT_LONG(Int):
    def __init__(self, alignment_border):
        super(ALIGNMENT_LONG, self).__init__(self, alignment_border)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ALIGNMENT_LONG, self).dump())[1])


@node_type('ALIGNMENT_WORD')
class ALIGNMENT_WORD(Int):
    def __init__(self, alignment_border):
        super(ALIGNMENT_WORD, self).__init__(self, alignment_border)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ALIGNMENT_WORD, self).dump())[1])


@node_type('ANNOTATION')
class ANNOTATION(A2lNode):
    __slots__ = 'annotation_label', 'annotation_origin', 'annotation_text', 

    def __init__(self, args):
        self.annotation_label = None
        self.annotation_origin = None
        self.annotation_text = None
        super(ANNOTATION, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('annotation_label',
                                                  'annotation_origin',
                                                  'annotation_text',
                                                  ))]


@node_type('ANNOTATION_LABEL')
class ANNOTATION_LABEL(String):
    def __init__(self, label):
        super(ANNOTATION_LABEL, self).__init__(self, label)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ANNOTATION_LABEL, self).dump())[1])


@node_type('ANNOTATION_ORIGIN')
class ANNOTATION_ORIGIN(String):
    def __init__(self, origin):
        super(ANNOTATION_ORIGIN, self).__init__(self, origin)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ANNOTATION_ORIGIN, self).dump())[1])


@node_type('ANNOTATION_TEXT')
class ANNOTATION_TEXT(A2lNode):
    __slots__ = 'text', 

    def __init__(self, args):
        self.text = List()
        super(ANNOTATION_TEXT, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('text',
                                                  ))]


@node_type('ARRAY_SIZE')
class ARRAY_SIZE(Int):
    def __init__(self, number):
        super(ARRAY_SIZE, self).__init__(self, number)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ARRAY_SIZE, self).dump())[1])


@node_type('ASAP2_VERSION')
class ASAP2_VERSION(A2lNode):
    __slots__ = 'version_no', 'upgrade_no', 

    def __init__(self, version_no, upgrade_no, ):
        self.version_no = Int(version_no)
        self.upgrade_no = Int(upgrade_no)
        super(ASAP2_VERSION, self).__init__()

    def positionals(self):
        return [e for e in (self.version_no,
                            self.upgrade_no,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('AXIS_DESCR')
class AXIS_DESCR(A2lNode):
    __slots__ = 'attribute', 'input_quantity', 'conversion', 'max_axis_points', 'lower_limit', 'upper_limit', 'read_only', 'format', 'annotation', 'axis_pts_ref', 'max_grad', 'monotony', 'byte_order', 'extended_limits', 'fix_axis_par', 'fix_axis_par_dist', 'fix_axis_par_list', 'deposit', 'curve_axis_ref', 

    def __init__(self, attribute, input_quantity, conversion, max_axis_points, lower_limit, upper_limit, args):
        self.attribute = enum_attribute(attribute)
        self.input_quantity = Ident(input_quantity)
        self.conversion = Ident(conversion)
        self.max_axis_points = Int(max_axis_points)
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        self.read_only = None
        self.format = None
        self.annotation = List()
        self.axis_pts_ref = None
        self.max_grad = None
        self.monotony = None
        self.byte_order = None
        self.extended_limits = None
        self.fix_axis_par = None
        self.fix_axis_par_dist = None
        self.fix_axis_par_list = None
        self.deposit = None
        self.curve_axis_ref = None
        super(AXIS_DESCR, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.attribute,
                            self.input_quantity,
                            self.conversion,
                            self.max_axis_points,
                            self.lower_limit,
                            self.upper_limit,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('read_only',
                                                  'format',
                                                  'annotation',
                                                  'axis_pts_ref',
                                                  'max_grad',
                                                  'monotony',
                                                  'byte_order',
                                                  'extended_limits',
                                                  'fix_axis_par',
                                                  'fix_axis_par_dist',
                                                  'fix_axis_par_list',
                                                  'deposit',
                                                  'curve_axis_ref',
                                                  ))]


@node_type('AXIS_PTS')
class AXIS_PTS(A2lNode):
    __slots__ = 'name', 'long_identifier', 'address', 'input_quantity', 'deposit', 'max_diff', 'conversion', 'max_axis_points', 'lower_limit', 'upper_limit', 'display_identifier', 'read_only', 'format', 'byte_order', 'function_list', 'ref_memory_segment', 'guard_rails', 'extended_limits', 'annotation', 'if_data', 'calibration_access', 'ecu_address_extension', 

    def __init__(self, name, long_identifier, address, input_quantity, deposit, max_diff, conversion, max_axis_points, lower_limit, upper_limit, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.address = Long(address)
        self.input_quantity = Ident(input_quantity)
        self.deposit = Ident(deposit)
        self.max_diff = Float(max_diff)
        self.conversion = Ident(conversion)
        self.max_axis_points = Int(max_axis_points)
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        self.display_identifier = None
        self.read_only = None
        self.format = None
        self.byte_order = None
        self.function_list = None
        self.ref_memory_segment = None
        self.guard_rails = None
        self.extended_limits = None
        self.annotation = List()
        self.if_data = dict()
        self.calibration_access = None
        self.ecu_address_extension = None
        super(AXIS_PTS, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.address,
                            self.input_quantity,
                            self.deposit,
                            self.max_diff,
                            self.conversion,
                            self.max_axis_points,
                            self.lower_limit,
                            self.upper_limit,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('display_identifier',
                                                  'read_only',
                                                  'format',
                                                  'byte_order',
                                                  'function_list',
                                                  'ref_memory_segment',
                                                  'guard_rails',
                                                  'extended_limits',
                                                  'annotation',
                                                  'if_data',
                                                  'calibration_access',
                                                  'ecu_address_extension',
                                                  ))]


@node_type('AXIS_PTS_REF')
class AXIS_PTS_REF(Ident):
    def __init__(self, axis_points):
        super(AXIS_PTS_REF, self).__init__(self, axis_points)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(AXIS_PTS_REF, self).dump())[1])


@node_type('AXIS_PTS_X')
class AXIS_PTS_X(A2lNode):
    __slots__ = 'position', 'data_type', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_PTS_X, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            self.index_incr,
                            self.addressing,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('AXIS_PTS_Y')
class AXIS_PTS_Y(A2lNode):
    __slots__ = 'position', 'data_type', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_PTS_Y, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            self.index_incr,
                            self.addressing,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('AXIS_PTS_Z')
class AXIS_PTS_Z(A2lNode):
    __slots__ = 'position', 'data_type', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_PTS_Z, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            self.index_incr,
                            self.addressing,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('AXIS_RESCALE_X')
class AXIS_RESCALE_X(A2lNode):
    __slots__ = 'position', 'data_type', 'max_number_of_rescale_pairs', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, max_number_of_rescale_pairs, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.max_number_of_rescale_pairs = Int(max_number_of_rescale_pairs)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_RESCALE_X, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            self.max_number_of_rescale_pairs,
                            self.index_incr,
                            self.addressing,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('AXIS_RESCALE_Y')
class AXIS_RESCALE_Y(A2lNode):
    __slots__ = 'position', 'data_type', 'max_number_of_rescale_pairs', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, max_number_of_rescale_pairs, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.max_number_of_rescale_pairs = Int(max_number_of_rescale_pairs)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_RESCALE_Y, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            self.max_number_of_rescale_pairs,
                            self.index_incr,
                            self.addressing,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('AXIS_RESCALE_Z')
class AXIS_RESCALE_Z(A2lNode):
    __slots__ = 'position', 'data_type', 'max_number_of_rescale_pairs', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, max_number_of_rescale_pairs, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.max_number_of_rescale_pairs = Int(max_number_of_rescale_pairs)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_RESCALE_Z, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            self.max_number_of_rescale_pairs,
                            self.index_incr,
                            self.addressing,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('BIT_MASK')
class BIT_MASK(Long):
    def __init__(self, mask):
        super(BIT_MASK, self).__init__(self, mask)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(BIT_MASK, self).dump())[1])


@node_type('BIT_OPERATION')
class BIT_OPERATION(A2lNode):
    __slots__ = 'left_shift', 'right_shift', 'sign_extend', 

    def __init__(self, args):
        self.left_shift = None
        self.right_shift = None
        self.sign_extend = None
        super(BIT_OPERATION, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('left_shift',
                                                  'right_shift',
                                                  'sign_extend',
                                                  ))]


@node_type('BYTE_ORDER')
class BYTE_ORDER(ByteOrder):
    def __init__(self, byte_order):
        super(BYTE_ORDER, self).__init__(self, byte_order)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(BYTE_ORDER, self).dump())[1])


@node_type('CALIBRATION_ACCESS')
class CALIBRATION_ACCESS(enum_type):
    def __init__(self, type):
        super(CALIBRATION_ACCESS, self).__init__(self, type)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(CALIBRATION_ACCESS, self).dump())[1])


@node_type('CALIBRATION_HANDLE')
class CALIBRATION_HANDLE(A2lNode):
    __slots__ = 'handle', 

    def __init__(self, args):
        self.handle = List()
        super(CALIBRATION_HANDLE, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('handle',
                                                  ))]


@node_type('CALIBRATION_METHOD')
class CALIBRATION_METHOD(A2lNode):
    __slots__ = 'method', 'version', 'calibration_handle', 

    def __init__(self, method, version, args):
        self.method = String(method)
        self.version = Long(version)
        self.calibration_handle = List()
        super(CALIBRATION_METHOD, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.method,
                            self.version,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('calibration_handle',
                                                  ))]


@node_type('CHARACTERISTIC')
class CHARACTERISTIC(A2lNode):
    __slots__ = 'name', 'long_identifier', 'type', 'address', 'deposit', 'max_diff', 'conversion', 'lower_limit', 'upper_limit', 'display_identifier', 'format', 'byte_order', 'bit_mask', 'function_list', 'number', 'extended_limits', 'read_only', 'guard_rails', 'map_list', 'max_refresh', 'dependent_characteristic', 'virtual_characteristic', 'ref_memory_segment', 'annotation', 'comparison_quantity', 'if_data', 'axis_descr', 'calibration_access', 'matrix_dim', 'ecu_address_extension', 

    def __init__(self, name, long_identifier, type, address, deposit, max_diff, conversion, lower_limit, upper_limit, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.type = enum_type(type)
        self.address = Long(address)
        self.deposit = Ident(deposit)
        self.max_diff = Float(max_diff)
        self.conversion = Ident(conversion)
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        self.display_identifier = None
        self.format = None
        self.byte_order = None
        self.bit_mask = None
        self.function_list = None
        self.number = None
        self.extended_limits = None
        self.read_only = None
        self.guard_rails = None
        self.map_list = None
        self.max_refresh = None
        self.dependent_characteristic = None
        self.virtual_characteristic = None
        self.ref_memory_segment = None
        self.annotation = List()
        self.comparison_quantity = None
        self.if_data = dict()
        self.axis_descr = List()
        self.calibration_access = None
        self.matrix_dim = None
        self.ecu_address_extension = None
        super(CHARACTERISTIC, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.type,
                            self.address,
                            self.deposit,
                            self.max_diff,
                            self.conversion,
                            self.lower_limit,
                            self.upper_limit,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('display_identifier',
                                                  'format',
                                                  'byte_order',
                                                  'bit_mask',
                                                  'function_list',
                                                  'number',
                                                  'extended_limits',
                                                  'read_only',
                                                  'guard_rails',
                                                  'map_list',
                                                  'max_refresh',
                                                  'dependent_characteristic',
                                                  'virtual_characteristic',
                                                  'ref_memory_segment',
                                                  'annotation',
                                                  'comparison_quantity',
                                                  'if_data',
                                                  'axis_descr',
                                                  'calibration_access',
                                                  'matrix_dim',
                                                  'ecu_address_extension',
                                                  ))]


@node_type('COEFFS')
class COEFFS(A2lNode):
    __slots__ = 'a', 'b', 'c', 'd', 'e', 'f', 

    def __init__(self, a, b, c, d, e, f, ):
        self.a = Float(a)
        self.b = Float(b)
        self.c = Float(c)
        self.d = Float(d)
        self.e = Float(e)
        self.f = Float(f)
        super(COEFFS, self).__init__()

    def positionals(self):
        return [e for e in (self.a,
                            self.b,
                            self.c,
                            self.d,
                            self.e,
                            self.f,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('COMPARISON_QUANTITY')
class COMPARISON_QUANTITY(Ident):
    def __init__(self, name):
        super(COMPARISON_QUANTITY, self).__init__(self, name)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(COMPARISON_QUANTITY, self).dump())[1])


@node_type('COMPU_METHOD')
class COMPU_METHOD(A2lNode):
    __slots__ = 'name', 'long_identifier', 'conversion_type', 'format', 'unit', 'formula', 'coeffs', 'compu_tab_ref', 'ref_unit', 

    def __init__(self, name, long_identifier, conversion_type, format, unit, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.conversion_type = enum_conversion_type(conversion_type)
        self.format = String(format)
        self.unit = String(unit)
        self.formula = None
        self.coeffs = None
        self.compu_tab_ref = None
        self.ref_unit = None
        super(COMPU_METHOD, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.conversion_type,
                            self.format,
                            self.unit,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('formula',
                                                  'coeffs',
                                                  'compu_tab_ref',
                                                  'ref_unit',
                                                  ))]


@node_type('COMPU_TAB')
class COMPU_TAB(A2lNode):
    __slots__ = 'name', 'long_identifier', 'conversion_type', 'number_value_pair', 'in_val_out_val', 'default_value', 

    def __init__(self, name, long_identifier, conversion_type, number_value_pair, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.conversion_type = enum_conversion_type(conversion_type)
        self.number_value_pair = Int(number_value_pair)
        self.in_val_out_val = List()  # TODO: change in_val_out_val by value_pair...
        self.default_value = None
        super(COMPU_TAB, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.conversion_type,
                            self.number_value_pair,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('in_val_out_val',
                                                  'default_value',
                                                  ))]


@node_type('COMPU_TAB_REF')
class COMPU_TAB_REF(Ident):
    def __init__(self, conversion_table):
        super(COMPU_TAB_REF, self).__init__(self, conversion_table)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(COMPU_TAB_REF, self).dump())[1])


@node_type('COMPU_VTAB')
class COMPU_VTAB(A2lNode):
    __slots__ = 'name', 'long_identifier', 'conversion_type', 'number_value_pair', 'in_val_out_val', 'default_value', 

    def __init__(self, name, long_identifier, conversion_type, number_value_pair, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.conversion_type = enum_conversion_type(conversion_type)
        self.number_value_pair = Int(number_value_pair)
        self.in_val_out_val = List()  # TODO: change in_val_out_val by value_pair...
        self.default_value = None
        super(COMPU_VTAB, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.conversion_type,
                            self.number_value_pair,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('in_val_out_val',
                                                  'default_value',
                                                  ))]


@node_type('COMPU_VTAB_RANGE')
class COMPU_VTAB_RANGE(A2lNode):
    __slots__ = 'name', 'long_identifier', 'number_value_triple', 'in_val_out_val', 'default_value', 

    def __init__(self, name, long_identifier, number_value_triple, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.number_value_triple = Int(number_value_triple)
        self.in_val_out_val = List()  # TODO: change in_val_out_val by value_pair...
        self.default_value = None
        super(COMPU_VTAB_RANGE, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.number_value_triple,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('in_val_out_val',
                                                  'default_value',
                                                  ))]


@node_type('CPU_TYPE')
class CPU_TYPE(String):
    def __init__(self, cpu_identifier):
        super(CPU_TYPE, self).__init__(self, cpu_identifier)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(CPU_TYPE, self).dump())[1])


@node_type('CURVE_AXIS_REF')
class CURVE_AXIS_REF(Ident):
    def __init__(self, curve_axis):
        super(CURVE_AXIS_REF, self).__init__(self, curve_axis)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(CURVE_AXIS_REF, self).dump())[1])


@node_type('CUSTOMER')
class CUSTOMER(String):
    def __init__(self, customer):
        super(CUSTOMER, self).__init__(self, customer)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(CUSTOMER, self).dump())[1])


@node_type('CUSTOMER_NO')
class CUSTOMER_NO(String):
    def __init__(self, number):
        super(CUSTOMER_NO, self).__init__(self, number)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(CUSTOMER_NO, self).dump())[1])


@node_type('DATA_SIZE')
class DATA_SIZE(Int):
    def __init__(self, size):
        super(DATA_SIZE, self).__init__(self, size)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(DATA_SIZE, self).dump())[1])


@node_type('DEFAULT_VALUE')
class DEFAULT_VALUE(String):
    def __init__(self, display_string):
        super(DEFAULT_VALUE, self).__init__(self, display_string)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(DEFAULT_VALUE, self).dump())[1])


@node_type('DEF_CHARACTERISTIC')
class DEF_CHARACTERISTIC(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(DEF_CHARACTERISTIC, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('DEPENDENT_CHARACTERISTIC')
class DEPENDENT_CHARACTERISTIC(A2lNode):
    __slots__ = 'formula', 'characteristic', 

    def __init__(self, formula, args):
        self.formula = String(formula)
        self.characteristic = List()  # TODO: defined as (Characteristic)* in specification, one or more?
        super(DEPENDENT_CHARACTERISTIC, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.formula,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('characteristic',
                                                  ))]


@node_type('DEPOSIT')
class DEPOSIT(enum_mode):
    def __init__(self, mode):
        super(DEPOSIT, self).__init__(self, mode)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(DEPOSIT, self).dump())[1])


@node_type('DISPLAY_IDENTIFIER')
class DISPLAY_IDENTIFIER(Ident):
    def __init__(self, display_name):
        super(DISPLAY_IDENTIFIER, self).__init__(self, display_name)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(DISPLAY_IDENTIFIER, self).dump())[1])


@node_type('DIST_OP_X')
class DIST_OP_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(DIST_OP_X, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('DIST_OP_Y')
class DIST_OP_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(DIST_OP_Y, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('DIST_OP_Z')
class DIST_OP_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(DIST_OP_Z, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('ECU')
class ECU(String):
    def __init__(self, control_unit):
        super(ECU, self).__init__(self, control_unit)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ECU, self).dump())[1])


@node_type('ECU_ADDRESS')
class ECU_ADDRESS(Long):
    def __init__(self, address):
        super(ECU_ADDRESS, self).__init__(self, address)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ECU_ADDRESS, self).dump())[1])


@node_type('ECU_ADDRESS_EXTENSION')
class ECU_ADDRESS_EXTENSION(Int):
    def __init__(self, extension):
        super(ECU_ADDRESS_EXTENSION, self).__init__(self, extension)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ECU_ADDRESS_EXTENSION, self).dump())[1])


@node_type('ECU_CALIBRATION_OFFSET')
class ECU_CALIBRATION_OFFSET(Long):
    def __init__(self, offset):
        super(ECU_CALIBRATION_OFFSET, self).__init__(self, offset)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ECU_CALIBRATION_OFFSET, self).dump())[1])


@node_type('EPK')
class EPK(String):
    def __init__(self, identifier):
        super(EPK, self).__init__(self, identifier)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(EPK, self).dump())[1])


@node_type('ERROR_MASK')
class ERROR_MASK(Long):
    def __init__(self, mask):
        super(ERROR_MASK, self).__init__(self, mask)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(ERROR_MASK, self).dump())[1])


@node_type('EXTENDED_LIMITS')
class EXTENDED_LIMITS(A2lNode):
    __slots__ = 'lower_limit', 'upper_limit', 

    def __init__(self, lower_limit, upper_limit, ):
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        super(EXTENDED_LIMITS, self).__init__()

    def positionals(self):
        return [e for e in (self.lower_limit,
                            self.upper_limit,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('FIX_AXIS_PAR')
class FIX_AXIS_PAR(A2lNode):
    __slots__ = 'offset', 'shift', 'numberapo', 

    def __init__(self, offset, shift, numberapo, ):
        self.offset = Int(offset)
        self.shift = Int(shift)
        self.numberapo = Int(numberapo)
        super(FIX_AXIS_PAR, self).__init__()

    def positionals(self):
        return [e for e in (self.offset,
                            self.shift,
                            self.numberapo,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('FIX_AXIS_PAR_DIST')
class FIX_AXIS_PAR_DIST(A2lNode):
    __slots__ = 'offset', 'distance', 'numberapo', 

    def __init__(self, offset, distance, numberapo, ):
        self.offset = Int(offset)
        self.distance = Int(distance)
        self.numberapo = Int(numberapo)
        super(FIX_AXIS_PAR_DIST, self).__init__()

    def positionals(self):
        return [e for e in (self.offset,
                            self.distance,
                            self.numberapo,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('FIX_AXIS_PAR_LIST')
class FIX_AXIS_PAR_LIST(A2lNode):
    __slots__ = 'axis_pts_value', 

    def __init__(self, args):
        self.axis_pts_value = List()
        super(FIX_AXIS_PAR_LIST, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('axis_pts_value',
                                                  ))]


@node_type('FIX_NO_AXIS_PTS_X')
class FIX_NO_AXIS_PTS_X(Int):
    def __init__(self, number_of_axis_points):
        super(FIX_NO_AXIS_PTS_X, self).__init__(self, number_of_axis_points)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(FIX_NO_AXIS_PTS_X, self).dump())[1])


@node_type('FIX_NO_AXIS_PTS_Y')
class FIX_NO_AXIS_PTS_Y(Int):
    def __init__(self, number_of_axis_points):
        super(FIX_NO_AXIS_PTS_Y, self).__init__(self, number_of_axis_points)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(FIX_NO_AXIS_PTS_Y, self).dump())[1])


@node_type('FIX_NO_AXIS_PTS_Z')
class FIX_NO_AXIS_PTS_Z(Int):
    def __init__(self, number_of_axis_points):
        super(FIX_NO_AXIS_PTS_Z, self).__init__(self, number_of_axis_points)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(FIX_NO_AXIS_PTS_Z, self).dump())[1])


@node_type('FNC_VALUES')
class FNC_VALUES(A2lNode):
    __slots__ = 'position', 'data_type', 'index_mode', 'addr_type', 

    def __init__(self, position, data_type, index_mode, addr_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.index_mode = enum_index_mode(index_mode)
        self.addr_type = AddrType(addr_type)
        super(FNC_VALUES, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            self.index_mode,
                            self.addr_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('FORMAT')
class FORMAT(String):
    def __init__(self, format_string):
        super(FORMAT, self).__init__(self, format_string)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(FORMAT, self).dump())[1])


@node_type('FORMULA')
class FORMULA(A2lNode):
    __slots__ = 'f', 'formula_inv', 

    def __init__(self, f, args):
        self.f = String(f)
        self.formula_inv = None
        super(FORMULA, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.f,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('formula_inv',
                                                  ))]


@node_type('FORMULA_INV')
class FORMULA_INV(String):
    def __init__(self, function):
        super(FORMULA_INV, self).__init__(self, function)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(FORMULA_INV, self).dump())[1])


@node_type('FRAME')
class FRAME(A2lNode):
    __slots__ = 'name', 'long_identifier', 'scaling_unit', 'rate', 'frame_measurement', 'if_data', 

    def __init__(self, name, long_identifier, scaling_unit, rate, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.scaling_unit = Int(scaling_unit)
        self.rate = Long(rate)
        self.frame_measurement = None
        self.if_data = dict()
        super(FRAME, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.scaling_unit,
                            self.rate,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('frame_measurement',
                                                  'if_data',
                                                  ))]


@node_type('FRAME_MEASUREMENT')
class FRAME_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(FRAME_MEASUREMENT, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('FUNCTION')
class FUNCTION(A2lNode):
    __slots__ = 'name', 'long_identifier', 'annotation', 'def_characteristic', 'ref_characteristic', 'in_measurement', 'out_measurement', 'loc_measurement', 'sub_function', 'function_version', 

    def __init__(self, name, long_identifier, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.annotation = List()
        self.def_characteristic = None
        self.ref_characteristic = None
        self.in_measurement = None
        self.out_measurement = None
        self.loc_measurement = None
        self.sub_function = None
        self.function_version = None
        super(FUNCTION, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('annotation',
                                                  'def_characteristic',
                                                  'ref_characteristic',
                                                  'in_measurement',
                                                  'out_measurement',
                                                  'loc_measurement',
                                                  'sub_function',
                                                  'function_version',
                                                  ))]


@node_type('FUNCTION_LIST')
class FUNCTION_LIST(A2lNode):
    __slots__ = 'name', 

    def __init__(self, args):
        self.name = List()
        super(FUNCTION_LIST, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('name',
                                                  ))]


@node_type('FUNCTION_VERSION')
class FUNCTION_VERSION(String):
    def __init__(self, version_identifier):
        super(FUNCTION_VERSION, self).__init__(self, version_identifier)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(FUNCTION_VERSION, self).dump())[1])


@node_type('GROUP')
class GROUP(A2lNode):
    __slots__ = 'group_name', 'group_long_identifier', 'annotation', 'root', 'ref_characteristic', 'ref_measurement', 'function_list', 'sub_group', 

    def __init__(self, group_name, group_long_identifier, args):
        self.group_name = Ident(group_name)
        self.group_long_identifier = String(group_long_identifier)
        self.annotation = List()
        self.root = None
        self.ref_characteristic = None
        self.ref_measurement = None
        self.function_list = None
        self.sub_group = None
        super(GROUP, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.group_name,
                            self.group_long_identifier,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('annotation',
                                                  'root',
                                                  'ref_characteristic',
                                                  'ref_measurement',
                                                  'function_list',
                                                  'sub_group',
                                                  ))]


@node_type('HEADER')
class HEADER(A2lNode):
    __slots__ = 'comment', 'version', 'project_no', 

    def __init__(self, comment, args):
        self.comment = String(comment)
        self.version = None
        self.project_no = None
        super(HEADER, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.comment,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('version',
                                                  'project_no',
                                                  ))]


@node_type('IDENTIFICATION')
class IDENTIFICATION(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(IDENTIFICATION, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('IN_MEASUREMENT')
class IN_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(IN_MEASUREMENT, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('LEFT_SHIFT')
class LEFT_SHIFT(Long):
    def __init__(self, bit_count):
        super(LEFT_SHIFT, self).__init__(self, bit_count)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(LEFT_SHIFT, self).dump())[1])


@node_type('LOC_MEASUREMENT')
class LOC_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(LOC_MEASUREMENT, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('MAP_LIST')
class MAP_LIST(A2lNode):
    __slots__ = 'name', 

    def __init__(self, args):
        self.name = List()
        super(MAP_LIST, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('name',
                                                  ))]


@node_type('MATRIX_DIM')
class MATRIX_DIM(A2lNode):
    __slots__ = 'x', 'y', 'z', 

    def __init__(self, x, y, z, ):
        self.x = Int(x)
        self.y = Int(y)
        self.z = Int(z)
        super(MATRIX_DIM, self).__init__()

    def positionals(self):
        return [e for e in (self.x,
                            self.y,
                            self.z,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('MAX_GRAD')
class MAX_GRAD(Float):
    def __init__(self, max_gradient):
        super(MAX_GRAD, self).__init__(self, max_gradient)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(MAX_GRAD, self).dump())[1])


@node_type('MAX_REFRESH')
class MAX_REFRESH(A2lNode):
    __slots__ = 'scaling_unit', 'rate', 

    def __init__(self, scaling_unit, rate, ):
        self.scaling_unit = Int(scaling_unit)
        self.rate = Long(rate)
        super(MAX_REFRESH, self).__init__()

    def positionals(self):
        return [e for e in (self.scaling_unit,
                            self.rate,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('MEASUREMENT')
class MEASUREMENT(A2lNode):
    __slots__ = 'name', 'long_identifier', 'data_type', 'conversion', 'resolution', 'accuracy', 'lower_limit', 'upper_limit', 'display_identifier', 'read_write', 'format', 'array_size', 'bit_mask', 'bit_operation', 'byte_order', 'max_refresh', 'virtual', 'function_list', 'ecu_address', 'error_mask', 'ref_memory_segment', 'annotation', 'if_data', 'matrix_dim', 'ecu_address_extension', 

    def __init__(self, name, long_identifier, data_type, conversion, resolution, accuracy, lower_limit, upper_limit, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.data_type = DataType(data_type)
        self.conversion = Ident(conversion)
        self.resolution = Int(resolution)
        self.accuracy = Float(accuracy)
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        self.display_identifier = None
        self.read_write = None
        self.format = None
        self.array_size = None
        self.bit_mask = None
        self.bit_operation = None
        self.byte_order = None
        self.max_refresh = None
        self.virtual = None
        self.function_list = None
        self.ecu_address = None
        self.error_mask = None
        self.ref_memory_segment = None
        self.annotation = List()
        self.if_data = dict()
        self.matrix_dim = None
        self.ecu_address_extension = None
        super(MEASUREMENT, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.data_type,
                            self.conversion,
                            self.resolution,
                            self.accuracy,
                            self.lower_limit,
                            self.upper_limit,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('display_identifier',
                                                  'read_write',
                                                  'format',
                                                  'array_size',
                                                  'bit_mask',
                                                  'bit_operation',
                                                  'byte_order',
                                                  'max_refresh',
                                                  'virtual',
                                                  'function_list',
                                                  'ecu_address',
                                                  'error_mask',
                                                  'ref_memory_segment',
                                                  'annotation',
                                                  'if_data',
                                                  'matrix_dim',
                                                  'ecu_address_extension',
                                                  ))]


@node_type('MEMORY_LAYOUT')
class MEMORY_LAYOUT(A2lNode):
    __slots__ = 'prg_type', 'address', 'size', 'offset', 'if_data', 

    def __init__(self, prg_type, address, size, offset, args):
        self.prg_type = enum_prg_type(prg_type)
        self.address = Long(address)
        self.size = Long(size)
        self.offset = Offset(offset)
        self.if_data = dict()
        super(MEMORY_LAYOUT, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.prg_type,
                            self.address,
                            self.size,
                            self.offset,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('if_data',
                                                  ))]


@node_type('MEMORY_SEGMENT')
class MEMORY_SEGMENT(A2lNode):
    __slots__ = 'name', 'long_identifier', 'prg_type', 'memory_type', 'attribute', 'address', 'size', 'offset', 'if_data', 

    def __init__(self, name, long_identifier, prg_type, memory_type, attribute, address, size, offset, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.prg_type = enum_prg_type(prg_type)
        self.memory_type = enum_memory_type(memory_type)
        self.attribute = enum_attribute(attribute)
        self.address = Long(address)
        self.size = Long(size)
        self.offset = Offset(offset)
        self.if_data = dict()
        super(MEMORY_SEGMENT, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.prg_type,
                            self.memory_type,
                            self.attribute,
                            self.address,
                            self.size,
                            self.offset,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('if_data',
                                                  ))]


@node_type('MODULE')
class MODULE(A2lNode):
    __slots__ = 'name', 'long_identifier', 'a2ml', 'mod_par', 'mod_common', 'if_data', 'characteristic', 'axis_pts', 'measurement', 'compu_method', 'compu_tab', 'compu_vtab', 'compu_vtab_range', 'function', 'group', 'record_layout', 'variant_coding', 'frame', 'user_rights', 'unit', 

    def __init__(self, name, long_identifier, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.a2ml = None
        self.mod_par = None
        self.mod_common = None
        self.if_data = dict()
        self.characteristic = List()
        self.axis_pts = List()
        self.measurement = List()
        self.compu_method = List()
        self.compu_tab = List()
        self.compu_vtab = List()
        self.compu_vtab_range = List()
        self.function = List()
        self.group = List()
        self.record_layout = List()
        self.variant_coding = None
        self.frame = None
        self.user_rights = List()
        self.unit = List()
        super(MODULE, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('a2ml',
                                                  'mod_par',
                                                  'mod_common',
                                                  'if_data',
                                                  'characteristic',
                                                  'axis_pts',
                                                  'measurement',
                                                  'compu_method',
                                                  'compu_tab',
                                                  'compu_vtab',
                                                  'compu_vtab_range',
                                                  'function',
                                                  'group',
                                                  'record_layout',
                                                  'variant_coding',
                                                  'frame',
                                                  'user_rights',
                                                  'unit',
                                                  ))]


@node_type('MOD_COMMON')
class MOD_COMMON(A2lNode):
    __slots__ = 'comment', 's_rec_layout', 'deposit', 'byte_order', 'data_size', 'alignment_byte', 'alignment_word', 'alignment_long', 'alignment_float32_ieee', 'alignment_float64_ieee', 

    def __init__(self, comment, args):
        self.comment = String(comment)
        self.s_rec_layout = None
        self.deposit = None
        self.byte_order = None
        self.data_size = None
        self.alignment_byte = None
        self.alignment_word = None
        self.alignment_long = None
        self.alignment_float32_ieee = None
        self.alignment_float64_ieee = None
        super(MOD_COMMON, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.comment,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('s_rec_layout',
                                                  'deposit',
                                                  'byte_order',
                                                  'data_size',
                                                  'alignment_byte',
                                                  'alignment_word',
                                                  'alignment_long',
                                                  'alignment_float32_ieee',
                                                  'alignment_float64_ieee',
                                                  ))]


@node_type('MOD_PAR')
class MOD_PAR(A2lNode):
    __slots__ = 'comment', 'version', 'addr_epk', 'epk', 'supplier', 'customer', 'customer_no', 'user', 'phone_no', 'ecu', 'cpu_type', 'no_of_interfaces', 'ecu_calibration_offset', 'calibration_method', 'memory_layout', 'memory_segment', 'system_constant', 

    def __init__(self, comment, args):
        self.comment = String(comment)
        self.version = None
        self.addr_epk = List()
        self.epk = None
        self.supplier = None
        self.customer = None
        self.customer_no = None
        self.user = None
        self.phone_no = None
        self.ecu = None
        self.cpu_type = None
        self.no_of_interfaces = None
        self.ecu_calibration_offset = None
        self.calibration_method = List()
        self.memory_layout = List()
        self.memory_segment = List()
        self.system_constant = List()
        super(MOD_PAR, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.comment,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('version',
                                                  'addr_epk',
                                                  'epk',
                                                  'supplier',
                                                  'customer',
                                                  'customer_no',
                                                  'user',
                                                  'phone_no',
                                                  'ecu',
                                                  'cpu_type',
                                                  'no_of_interfaces',
                                                  'ecu_calibration_offset',
                                                  'calibration_method',
                                                  'memory_layout',
                                                  'memory_segment',
                                                  'system_constant',
                                                  ))]


@node_type('MONOTONY')
class MONOTONY(monotony_enum):
    def __init__(self, monotony):
        super(MONOTONY, self).__init__(self, monotony)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(MONOTONY, self).dump())[1])


@node_type('NO_AXIS_PTS_X')
class NO_AXIS_PTS_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_AXIS_PTS_X, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('NO_AXIS_PTS_Y')
class NO_AXIS_PTS_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_AXIS_PTS_Y, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('NO_AXIS_PTS_Z')
class NO_AXIS_PTS_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_AXIS_PTS_Z, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('NO_OF_INTERFACES')
class NO_OF_INTERFACES(Int):
    def __init__(self, number_of_interfaces):
        super(NO_OF_INTERFACES, self).__init__(self, number_of_interfaces)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(NO_OF_INTERFACES, self).dump())[1])


@node_type('NO_RESCALE_X')
class NO_RESCALE_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_RESCALE_X, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('NO_RESCALE_Y')
class NO_RESCALE_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_RESCALE_Y, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('NO_RESCALE_Z')
class NO_RESCALE_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_RESCALE_Z, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('NUMBER')
class NUMBER(Int):
    def __init__(self, number):
        super(NUMBER, self).__init__(self, number)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(NUMBER, self).dump())[1])


@node_type('OFFSET_X')
class OFFSET_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(OFFSET_X, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('OFFSET_Y')
class OFFSET_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(OFFSET_Y, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('OFFSET_Z')
class OFFSET_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(OFFSET_Z, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('OUT_MEASUREMENT')
class OUT_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(OUT_MEASUREMENT, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('PHONE_NO')
class PHONE_NO(String):
    def __init__(self, phone_number):
        super(PHONE_NO, self).__init__(self, phone_number)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(PHONE_NO, self).dump())[1])


@node_type('PROJECT')
class PROJECT(A2lNode):
    __slots__ = 'name', 'long_identifier', 'header', 'module', 

    def __init__(self, name, long_identifier, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.header = None
        self.module = List()
        super(PROJECT, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('header',
                                                  'module',
                                                  ))]


@node_type('PROJECT_NO')
class PROJECT_NO(Ident):
    def __init__(self, project_number):
        super(PROJECT_NO, self).__init__(self, project_number)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(PROJECT_NO, self).dump())[1])


@node_type('RECORD_LAYOUT')
class RECORD_LAYOUT(A2lNode):
    __slots__ = 'name', 'fnc_values', 'identification', 'axis_pts_x', 'axis_pts_y', 'axis_pts_z', 'axis_rescale_x', 'axis_rescale_y', 'axis_rescale_z', 'no_axis_pts_x', 'no_axis_pts_y', 'no_axis_pts_z', 'no_rescale_x', 'no_rescale_y', 'no_rescale_z', 'fix_no_axis_pts_x', 'fix_no_axis_pts_y', 'fix_no_axis_pts_z', 'src_addr_x', 'src_addr_y', 'src_addr_z', 'rip_addr_x', 'rip_addr_y', 'rip_addr_z', 'rip_addr_w', 'shift_op_x', 'shift_op_y', 'shift_op_z', 'offset_x', 'offset_y', 'offset_z', 'dist_op_x', 'dist_op_y', 'dist_op_z', 'alignment_byte', 'alignment_word', 'alignment_long', 'alignment_float32_ieee', 'alignment_float64_ieee', 'reserved', 

    def __init__(self, name, args):
        self.name = Ident(name)
        self.fnc_values = None
        self.identification = None
        self.axis_pts_x = None
        self.axis_pts_y = None
        self.axis_pts_z = None
        self.axis_rescale_x = None
        self.axis_rescale_y = None
        self.axis_rescale_z = None
        self.no_axis_pts_x = None
        self.no_axis_pts_y = None
        self.no_axis_pts_z = None
        self.no_rescale_x = None
        self.no_rescale_y = None
        self.no_rescale_z = None
        self.fix_no_axis_pts_x = None
        self.fix_no_axis_pts_y = None
        self.fix_no_axis_pts_z = None
        self.src_addr_x = None
        self.src_addr_y = None
        self.src_addr_z = None
        self.rip_addr_x = None
        self.rip_addr_y = None
        self.rip_addr_z = None
        self.rip_addr_w = None
        self.shift_op_x = None
        self.shift_op_y = None
        self.shift_op_z = None
        self.offset_x = None
        self.offset_y = None
        self.offset_z = None
        self.dist_op_x = None
        self.dist_op_y = None
        self.dist_op_z = None
        self.alignment_byte = None
        self.alignment_word = None
        self.alignment_long = None
        self.alignment_float32_ieee = None
        self.alignment_float64_ieee = None
        self.reserved = List()
        super(RECORD_LAYOUT, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('fnc_values',
                                                  'identification',
                                                  'axis_pts_x',
                                                  'axis_pts_y',
                                                  'axis_pts_z',
                                                  'axis_rescale_x',
                                                  'axis_rescale_y',
                                                  'axis_rescale_z',
                                                  'no_axis_pts_x',
                                                  'no_axis_pts_y',
                                                  'no_axis_pts_z',
                                                  'no_rescale_x',
                                                  'no_rescale_y',
                                                  'no_rescale_z',
                                                  'fix_no_axis_pts_x',
                                                  'fix_no_axis_pts_y',
                                                  'fix_no_axis_pts_z',
                                                  'src_addr_x',
                                                  'src_addr_y',
                                                  'src_addr_z',
                                                  'rip_addr_x',
                                                  'rip_addr_y',
                                                  'rip_addr_z',
                                                  'rip_addr_w',
                                                  'shift_op_x',
                                                  'shift_op_y',
                                                  'shift_op_z',
                                                  'offset_x',
                                                  'offset_y',
                                                  'offset_z',
                                                  'dist_op_x',
                                                  'dist_op_y',
                                                  'dist_op_z',
                                                  'alignment_byte',
                                                  'alignment_word',
                                                  'alignment_long',
                                                  'alignment_float32_ieee',
                                                  'alignment_float64_ieee',
                                                  'reserved',
                                                  ))]


@node_type('REF_CHARACTERISTIC')
class REF_CHARACTERISTIC(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(REF_CHARACTERISTIC, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('REF_GROUP')
class REF_GROUP(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(REF_GROUP, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('REF_MEASUREMENT')
class REF_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(REF_MEASUREMENT, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('REF_MEMORY_SEGMENT')
class REF_MEMORY_SEGMENT(Ident):
    def __init__(self, name):
        super(REF_MEMORY_SEGMENT, self).__init__(self, name)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(REF_MEMORY_SEGMENT, self).dump())[1])


@node_type('REF_UNIT')
class REF_UNIT(Ident):
    def __init__(self, unit):
        super(REF_UNIT, self).__init__(self, unit)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(REF_UNIT, self).dump())[1])


@node_type('RESERVED')
class RESERVED(A2lNode):
    __slots__ = 'position', 'data_size', 

    def __init__(self, position, data_size, ):
        self.position = Int(position)
        self.data_size = DataSize(data_size)
        super(RESERVED, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_size,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('RIGHT_SHIFT')
class RIGHT_SHIFT(Long):
    def __init__(self, bit_count):
        super(RIGHT_SHIFT, self).__init__(self, bit_count)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(RIGHT_SHIFT, self).dump())[1])


@node_type('RIP_ADDR_W')
class RIP_ADDR_W(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(RIP_ADDR_W, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('RIP_ADDR_X')
class RIP_ADDR_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(RIP_ADDR_X, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('RIP_ADDR_Y')
class RIP_ADDR_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(RIP_ADDR_Y, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('RIP_ADDR_Z')
class RIP_ADDR_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(RIP_ADDR_Z, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('SHIFT_OP_X')
class SHIFT_OP_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SHIFT_OP_X, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('SHIFT_OP_Y')
class SHIFT_OP_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SHIFT_OP_Y, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('SHIFT_OP_Z')
class SHIFT_OP_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SHIFT_OP_Z, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('SI_EXPONENTS')
class SI_EXPONENTS(A2lNode):
    __slots__ = 'length', 'mass', 'time', 'electric_current', 'temperature', 'amount_of_substance', 'luminous_intensity', 

    def __init__(self, length, mass, time, electric_current, temperature, amount_of_substance, luminous_intensity, ):
        self.length = Int(length)
        self.mass = Int(mass)
        self.time = Int(time)
        self.electric_current = Int(electric_current)
        self.temperature = Int(temperature)
        self.amount_of_substance = Int(amount_of_substance)
        self.luminous_intensity = Int(luminous_intensity)
        super(SI_EXPONENTS, self).__init__()

    def positionals(self):
        return [e for e in (self.length,
                            self.mass,
                            self.time,
                            self.electric_current,
                            self.temperature,
                            self.amount_of_substance,
                            self.luminous_intensity,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('SRC_ADDR_X')
class SRC_ADDR_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SRC_ADDR_X, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('SRC_ADDR_Y')
class SRC_ADDR_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SRC_ADDR_Y, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('SRC_ADDR_Z')
class SRC_ADDR_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SRC_ADDR_Z, self).__init__()

    def positionals(self):
        return [e for e in (self.position,
                            self.data_type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('SUB_FUNCTION')
class SUB_FUNCTION(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(SUB_FUNCTION, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('SUB_GROUP')
class SUB_GROUP(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = List()
        super(SUB_GROUP, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('identifier',
                                                  ))]


@node_type('SUPPLIER')
class SUPPLIER(String):
    def __init__(self, manufacturer):
        super(SUPPLIER, self).__init__(self, manufacturer)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(SUPPLIER, self).dump())[1])


@node_type('SYSTEM_CONSTANT')
class SYSTEM_CONSTANT(A2lNode):
    __slots__ = 'name', 'value', 

    def __init__(self, name, value, ):
        self.name = String(name)
        self.value = String(value)
        super(SYSTEM_CONSTANT, self).__init__()

    def positionals(self):
        return [e for e in (self.name,
                            self.value,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('S_REC_LAYOUT')
class S_REC_LAYOUT(Ident):
    def __init__(self, name):
        super(S_REC_LAYOUT, self).__init__(self, name)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(S_REC_LAYOUT, self).dump())[1])


@node_type('UNIT')
class UNIT(A2lNode):
    __slots__ = 'name', 'long_identifier', 'display', 'type', 'si_exponents', 'ref_unit', 'unit_conversion', 

    def __init__(self, name, long_identifier, display, type, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.display = String(display)
        self.type = enum_type(type)
        self.si_exponents = None
        self.ref_unit = None
        self.unit_conversion = None
        super(UNIT, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.display,
                            self.type,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('si_exponents',
                                                  'ref_unit',
                                                  'unit_conversion',
                                                  ))]


@node_type('UNIT_CONVERSION')
class UNIT_CONVERSION(A2lNode):
    __slots__ = 'gradient', 'offset', 

    def __init__(self, gradient, offset, ):
        self.gradient = Float(gradient)
        self.offset = Float(offset)
        super(UNIT_CONVERSION, self).__init__()

    def positionals(self):
        return [e for e in (self.gradient,
                            self.offset,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(())]


@node_type('USER')
class USER(String):
    def __init__(self, user_name):
        super(USER, self).__init__(self, user_name)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(USER, self).dump())[1])


@node_type('USER_RIGHTS')
class USER_RIGHTS(A2lNode):
    __slots__ = 'user_level_id', 'ref_group', 'read_only', 

    def __init__(self, user_level_id, args):
        self.user_level_id = Ident(user_level_id)
        self.ref_group = List()
        self.read_only = None
        super(USER_RIGHTS, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.user_level_id,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('ref_group',
                                                  'read_only',
                                                  ))]


@node_type('VARIANT_CODING')
class VARIANT_CODING(A2lNode):
    __slots__ = 'var_separator', 'var_naming', 'var_criterion', 'var_forbidden_comb', 'var_characteristic', 

    def __init__(self, args):
        self.var_separator = None
        self.var_naming = None
        self.var_criterion = List()
        self.var_forbidden_comb = List()
        self.var_characteristic = List()
        super(VARIANT_CODING, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('var_separator',
                                                  'var_naming',
                                                  'var_criterion',
                                                  'var_forbidden_comb',
                                                  'var_characteristic',
                                                  ))]


@node_type('VAR_ADDRESS')
class VAR_ADDRESS(A2lNode):
    __slots__ = 'address', 

    def __init__(self, args):
        self.address = List()
        super(VAR_ADDRESS, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('address',
                                                  ))]


@node_type('VAR_CHARACTERISTIC')
class VAR_CHARACTERISTIC(A2lNode):
    __slots__ = 'name', 'criterion_name', 'var_address', 

    def __init__(self, name, args):
        self.name = Ident(name)
        self.criterion_name = List()
        self.var_address = None
        super(VAR_CHARACTERISTIC, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('criterion_name',
                                                  'var_address',
                                                  ))]


@node_type('VAR_CRITERION')
class VAR_CRITERION(A2lNode):
    __slots__ = 'name', 'long_identifier', 'value', 'var_measurement', 'var_selection_characteristic', 

    def __init__(self, name, long_identifier, value, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.value = IdentList(value)
        self.var_measurement = None
        self.var_selection_characteristic = None
        super(VAR_CRITERION, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.name,
                            self.long_identifier,
                            self.value,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('var_measurement',
                                                  'var_selection_characteristic',
                                                  ))]


@node_type('VAR_FORBIDDEN_COMB')
class VAR_FORBIDDEN_COMB(A2lNode):
    __slots__ = 'criterion', 

    def __init__(self, args):
        self.criterion = List()
        super(VAR_FORBIDDEN_COMB, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('criterion',
                                                  ))]


@node_type('VAR_MEASUREMENT')
class VAR_MEASUREMENT(Ident):
    def __init__(self, name):
        super(VAR_MEASUREMENT, self).__init__(self, name)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(VAR_MEASUREMENT, self).dump())[1])


@node_type('VAR_NAMING')
class VAR_NAMING(enum_tag):
    def __init__(self, tag):
        super(VAR_NAMING, self).__init__(self, tag)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(VAR_NAMING, self).dump())[1])


@node_type('VAR_SELECTION_CHARACTERISTIC')
class VAR_SELECTION_CHARACTERISTIC(Ident):
    def __init__(self, name):
        super(VAR_SELECTION_CHARACTERISTIC, self).__init__(self, name)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(VAR_SELECTION_CHARACTERISTIC, self).dump())[1])


@node_type('VAR_SEPARATOR')
class VAR_SEPARATOR(String):
    def __init__(self, separator):
        super(VAR_SEPARATOR, self).__init__(self, separator)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(VAR_SEPARATOR, self).dump())[1])


@node_type('VERSION')
class VERSION(String):
    def __init__(self, version_identifier):
        super(VERSION, self).__init__(self, version_identifier)

    @property
    def node(self):
        return self._node

    def dump(self, n=0):
        yield n, '{} {}'.format(self.node, next(super(VERSION, self).dump())[1])


@node_type('VIRTUAL')
class VIRTUAL(A2lNode):
    __slots__ = 'measuring_channel', 

    def __init__(self, args):
        self.measuring_channel = List()
        super(VIRTUAL, self).__init__(*args)

    def positionals(self):
        return [e for e in ()]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('measuring_channel',
                                                  ))]


@node_type('VIRTUAL_CHARACTERISTIC')
class VIRTUAL_CHARACTERISTIC(A2lNode):
    __slots__ = 'formula', 'characteristic', 

    def __init__(self, formula, args):
        self.formula = String(formula)
        self.characteristic = List()
        super(VIRTUAL_CHARACTERISTIC, self).__init__(*args)

    def positionals(self):
        return [e for e in (self.formula,
                            )]

    def keywords(self):
        return [getattr(self, e) for e in sorted(('characteristic',
                                                  ))]

