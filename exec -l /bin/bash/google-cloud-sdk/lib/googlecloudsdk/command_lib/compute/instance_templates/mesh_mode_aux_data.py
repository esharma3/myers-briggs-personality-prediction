# -*- coding: utf-8 -*- #
# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Auxiliary data for implementing Mesh mode flags Instance Templates."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import enum


class MeshModes(str, enum.Enum):
  ON = 'ON'
  OFF = 'OFF'


# Don't put sudo when running mesh-agent-bootstrap.sh, as exported variables
# don't get passed to the script when run with sudo. It's not a problem
# because all commands inside mesh-agent-bootstrap.sh are run with sudo anyway.
startup_script = """#! /bin/bash
export MESH_AGENT_DIRECTORY=$(mktemp -d)
sudo gsutil cp gs://gce-mesh/mesh-agent/releases/mesh-agent-0.1.tgz ${MESH_AGENT_DIRECTORY}
sudo tar -xzf ${MESH_AGENT_DIRECTORY}/mesh-agent-0.1.tgz -C ${MESH_AGENT_DIRECTORY}
${MESH_AGENT_DIRECTORY}/mesh-agent/mesh-agent-bootstrap.sh"""
