# DO NOT EDIT. This file was generated with:
#
# $ edb gen-schema-mixins

"""Type definitions for generated methods on schema classes"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from edb.schema import schema as s_schema
from edb.schema import getter as s_getter

from edb.schema import objects
from edb.schema import expr
from edb.edgeql import qltypes


class AccessPolicyMixin:

    def get_condition(
        self, schema: 's_schema.Schema'
    ) -> 'expr.Expression':
        return s_getter.get_field_value(  # type: ignore
            self, schema, 'condition'    # type: ignore
        )

    def get_expr(
        self, schema: 's_schema.Schema'
    ) -> 'expr.Expression':
        return s_getter.get_field_value(  # type: ignore
            self, schema, 'expr'    # type: ignore
        )

    def get_action(
        self, schema: 's_schema.Schema'
    ) -> 'qltypes.AccessPolicyAction':
        return s_getter.get_field_value(  # type: ignore
            self, schema, 'action'    # type: ignore
        )

    def get_access_kinds(
        self, schema: 's_schema.Schema'
    ) -> 'objects.MultiPropSet[qltypes.AccessKind]':
        return s_getter.get_field_value(  # type: ignore
            self, schema, 'access_kinds'    # type: ignore
        )

    def get_subject(
        self, schema: 's_schema.Schema'
    ) -> 'objects.InheritingObject':
        return s_getter.get_field_value(  # type: ignore
            self, schema, 'subject'    # type: ignore
        )

    def get_errmessage(
        self, schema: 's_schema.Schema'
    ) -> 'str':
        return s_getter.get_field_value(  # type: ignore
            self, schema, 'errmessage'    # type: ignore
        )

    def get_owned(
        self, schema: 's_schema.Schema'
    ) -> 'bool':
        return s_getter.get_field_value(  # type: ignore
            self, schema, 'owned'    # type: ignore
        )
