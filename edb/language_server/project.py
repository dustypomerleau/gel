#
# This source file is part of the EdgeDB open source project.
#
# Copyright 2008-present MagicStack Inc. and the EdgeDB authors.
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

from typing import cast, Any
from pathlib import Path
import dataclasses
import tomllib


@dataclasses.dataclass(kw_only=True, frozen=True)
class Instance:
    server_version: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Project:
    schema_dir: Path


@dataclasses.dataclass(kw_only=True, frozen=True)
class Manifest:
    instance: Instance | None
    project: Project | None
    # hooks: Option<Hooks>,
    # watch: Vec<WatchScript>,


def read_manifest(project_dir: Path) -> tuple[Manifest, Path]:
    try:
        path = project_dir / 'gel.toml'
        with open(path, 'rb') as f:
            manifest_dict = tomllib.load(f)
    except FileNotFoundError:
        path = project_dir / 'edgedb.toml'
        with open(path, 'rb') as f:
            manifest_dict = tomllib.load(f)

    return (_load_manifest(manifest_dict), path)


def _load_manifest(manifest_dict: Any) -> Manifest:
    instance = None
    if 'instance' in manifest_dict:
        instance = _load_instance(manifest_dict['instance'])
    elif 'edgedb' in manifest_dict:
        instance = _load_instance(manifest_dict['edgedb'])

    project = None
    if 'project' in manifest_dict:
        project = _load_project(manifest_dict['project'])

    return Manifest(
        instance=instance,
        project=project,
    )


def _load_instance(instance_dict: Any) -> Instance | None:
    server_version = None
    if 'server-version' in instance_dict:
        server_version = cast(str, instance_dict['server-version'])
    else:
        return None

    return Instance(server_version=server_version)


def _load_project(project_dict: Any) -> Project | None:
    schema_dir = None
    if 'schema-dir' in project_dict:
        schema_dir = Path(project_dict['schema-dir'])
    else:
        return None

    return Project(schema_dir=schema_dir)
