# DO NOT EDIT. This file was generated with:
#
# $ edb gen-schema-mixins

"""Type definitions for generated methods on schema classes"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from edb.schema import schema as s_schema
from edb.schema import getter as s_getter

from edb.schema import objects
from edb.schema import pointers


class SourceMixin:

    def get_pointers(
        self, schema: 's_schema.Schema'
    ) -> 'objects.ObjectIndexByUnqualifiedName[pointers.Pointer]':
        return s_getter.get_field_value(  # type: ignore
            self, schema, 'pointers'    # type: ignore
        )
