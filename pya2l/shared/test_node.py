"""
@project: pya2l
@file: node_test.py
@author: Guillaume Sottas
@date: 28.12.2018
"""

from pya2l.shared.node import ASTNode


def test_init():
    class A(ASTNode):
        __slots__ = '_d', '_l', '_n'

        def __init__(self, args):
            self._d = dict()
            self._l = list()
            self._n = None
            super(A, self).__init__(*args)

    obj = A((
        ('_d', 0),
        ('_l', 1),
        ('_l', 2),
        ('_n', 3)
    ))

    assert obj._d == 0
    assert obj._l == [1, 2]
    assert obj._n == 3


def test_parent_children_properties():
    class Parent(ASTNode):
        __slots__ = 'child',

        def __init__(self, child):
            self.child = list()
            super(Parent, self).__init__(*child)

    class Child(ASTNode):
        __slots__ = 'n',

        def __init__(self, n):
            self.n = n
            super(Child, self).__init__()

    child_0 = Child(0)
    child_1 = Child(1)
    parent = Parent((('child', child_0), ('child', child_1)))

    assert parent.children == [child_0, child_1]
    assert parent.parent is None
    assert child_0.children == []
    assert child_1.children == []
    assert child_0.parent == parent
    assert child_1.parent == parent


def test_eq_and_ne_operator():
    class A(ASTNode):
        __slots__ = 'a',

        def __init__(self, a):
            self.a = a
            super(A, self).__init__()

    class B(ASTNode):
        __slots__ = 'b',

        def __init__(self, b):
            self.b = b
            super(B, self).__init__()

    class C(ASTNode):
        __slots__ = 'a',

        def __init__(self, a):
            self.a = a
            super(C, self).__init__()

    class D(ASTNode):
        __slots__ = 'a', 'b'

        def __init__(self, a, b=0):
            self.a = a
            self.b = b
            super(D, self).__init__()

    assert A(0) != B(0)
    assert C(0) != C(1)
    assert C(0) == C(0)
    assert A(0) == C(0)
    assert A(0) != D(0)


def test_nodes():
    class Parent(ASTNode):
        _node = 'Parent'
        __slots__ = 'child',

        def __init__(self, child):
            self.child = list()
            super(Parent, self).__init__(*child)

    class Child(ASTNode):
        _node = 'Child'
        __slots__ = 'n',

        def __init__(self, n):
            self.n = n
            super(Child, self).__init__()

    child_0 = Child(0)
    child_1 = Child(1)
    parent = Parent((('child', child_0), ('child', child_1)))

    assert parent.nodes('invalid name') == []
    assert parent.nodes('Child') == [child_0, child_1]


def test_get_dict():
    class A(ASTNode):
        _node = 'A'
        __slots__ = 'prop', 'sub_node'

        def __init__(self, prop, sub_node):
            self.prop = prop
            self.sub_node = sub_node
            super(A, self).__init__()

    class B(ASTNode):
        _node = 'B'
        __slots__ = 'list_property',

        def __init__(self, list_property):
            self.list_property = list_property
            super(B, self).__init__()

    class C(ASTNode):
        _node = 'C'

        def __init__(self):
            super(C, self).__init__()

    assert A(1, A(2, B([3, C()]))).dict() == {
        'node': 'A',
        'prop': 1,
        'sub_node': {
            'node': 'A',
            'prop': 2,
            'sub_node': {
                'node': 'B',
                'list_property': [3, {
                    'node': 'C'
                }]
            }
        }}