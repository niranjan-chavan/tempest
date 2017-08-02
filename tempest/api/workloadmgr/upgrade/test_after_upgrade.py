# Copyright 2014 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.api.workloadmgr import base
from tempest import config
from tempest import test
import json
import sys
from tempest import api
from oslo_log import log as logging
from tempest.common import waiters
from tempest import tvaultconf
from tempest.api.workloadmgr.cli.config import command_argument_string
from tempest.api.workloadmgr.cli.util import cli_parser
from tempest import reporting

LOG = logging.getLogger(__name__)
CONF = config.CONF


class WorkloadsTest(base.BaseWorkloadmgrTest):

    credentials = ['primary']

    @classmethod
    def setup_clients(cls):
        super(WorkloadsTest, cls).setup_clients()
        cls.client = cls.os.wlm_client
	reporting.add_test_script(str(__name__))

    @test.attr(type='smoke')
    @test.idempotent_id('9fe07175-912e-49a5-a629-5f52eeada4c9')
    def test_after_upgrade(self):
	#Import workloads using CLI command
        rc = cli_parser.cli_returncode(command_argument_string.workload_import)
        if rc != 0:
            reporting.add_test_step("Execute workload-importworkloads command", tvaultconf.FAIL)
            raise Exception("Command did not execute correctly")
        else:
            reporting.add_test_step("Execute workload-importworkloads command", tvaultconf.PASS)
            LOG.debug("Command executed correctly")

	#Get list of workloads imported
	self.workloads = self.getWorkloadList()
	LOG.debug("Workload list after import: " + str(self.workloads))

	#Verify if workload created before upgrade is imported
	self.workload_id_before_upgrade = self.read_upgrade_data("workload_id")
	LOG.debug("Workload id before upgrade: " + str(self.workload_id_before_upgrade))
	if(str(self.workload_id_before_upgrade) in self.workloads):
	    reporting.add_test_step("Verify workload", tvaultconf.PASS)
        else:
	    reporting.add_test_step("Verify workload", tvaultconf.FAIL)

	#Get list of snapshots imported
	self.snapshots = self.getSnapshotList()
	LOG.debug("Snapshot list after import: " + str(self.snapshots))

	#Verify if snapshots created before upgrade are imported
	self.snapshot_before_upgrade = self.read_upgrade_data("full_snapshot_id")
	LOG.debug("Snapshot before upgrade: " + str(self.snapshot_before_upgrade))
	if(str(self.snapshot_before_upgrade) in self.snapshots):
	    reporting.add_test_step("Verify snapshot", tvaultconf.PASS)
	else:
	    reporting.add_test_step("Verify snapshot", tvaultconf.FAIL)
