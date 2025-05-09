#
# This source file is part of the EdgeDB open source project.
#
# Copyright 2016-present MagicStack Inc. and the EdgeDB authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

include "./pgcon_sql.pxd"

cimport cython
cimport cpython

from libc.stdint cimport int8_t, uint8_t, int16_t, uint16_t, \
                         int32_t, uint32_t, int64_t, uint64_t

from edb.server.pgproto.pgproto cimport (
    WriteBuffer,
    ReadBuffer,
    FRBuffer,
)

from edb.server.dbview cimport dbview
from edb.server.pgproto.debug cimport PG_DEBUG

from edb.server.cache cimport stmt_cache


cdef enum PGTransactionStatus:
    PQTRANS_IDLE = 0                 # connection idle
    PQTRANS_ACTIVE = 1               # command in progress
    PQTRANS_INTRANS = 2              # idle, within transaction block
    PQTRANS_INERROR = 3              # idle, within failed transaction
    PQTRANS_UNKNOWN = 4              # cannot determine status


cdef enum PGAuthenticationState:
    PGAUTH_SUCCESSFUL = 0
    PGAUTH_REQUIRED_KERBEROS = 2
    PGAUTH_REQUIRED_PASSWORD = 3
    PGAUTH_REQUIRED_PASSWORDMD5 = 5
    PGAUTH_REQUIRED_SCMCRED = 6
    PGAUTH_REQUIRED_GSS = 7
    PGAUTH_REQUIRED_GSS_CONTINUE = 8
    PGAUTH_REQUIRED_SSPI = 9
    PGAUTH_REQUIRED_SASL = 10
    PGAUTH_SASL_CONTINUE = 11
    PGAUTH_SASL_FINAL = 12


@cython.final
cdef class PGConnection:

    cdef:
        ReadBuffer buffer

        object loop
        str dbname

        object transport
        object msg_waiter

        readonly bint connected
        object connected_fut

        int32_t waiting_for_sync
        PGTransactionStatus xact_status

        public int32_t backend_pid
        public int32_t backend_secret
        public object parameter_status

        readonly object aborted_with_error

        stmt_cache.StatementsCache prep_stmts
        list last_parse_prep_stmts

        list log_listeners

        bint debug

        public object connection
        public object addr
        object server
        object tenant
        bint is_system_db
        bint close_requested

        readonly bint idle

        object cancel_fut

        bint _is_ssl

        public object pinned_by

        object last_state
        bint state_reset_needs_commit
        public object last_init_con_data

        str last_indirect_return

        PGSQLConnection _sql

    cdef before_command(self)

    cdef write(self, buf)
    cdef write_sync(self, WriteBuffer outbuf)

    cdef parse_error_message(self)
    cdef char parse_sync_message(self)
    cdef parse_parameter_status_message(self)

    cdef parse_notification(self)
    cdef fallthrough(self)
    cdef fallthrough_idle(self)

    cdef bint before_prepare(
        self, bytes stmt_name, int dbver, WriteBuffer outbuf)
    cdef write_sync(self, WriteBuffer outbuf)
    cdef send_sync(self)

    cdef make_clean_stmt_message(self, bytes stmt_name)
    cdef send_query_unit_group(
        self, object query_unit_group, bint sync,
        object bind_datas, bytes state,
        ssize_t start, ssize_t end, int dbver, object parse_array,
        object query_prefix,
        bint needs_commit_state,
    )

    cdef _rewrite_copy_data(
        self,
        WriteBuffer wbuf,
        char *data,
        ssize_t data_len,
        ssize_t ncols,
        tuple elide_cols,
        dict type_id_map,
        tuple data_mending_desc,
    )

    cdef _mend_copy_datum(
        self,
        WriteBuffer wbuf,
        FRBuffer *rbuf,
        object mending_desc,
        dict type_id_map,
    )

    cdef inline str get_tenant_label(self)
    cpdef set_stmt_cache_size(self, int maxsize)
