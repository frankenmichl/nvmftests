# Copyright (c) 2016-2017 Western Digital Corporation or its affiliates.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.
#
#   Author: Chaitanya Kulkarni <chaitanya.kulkarni@wdc.com>
#
"""
NVMF Create/Delete Host :-

    1. From the config file create Target.
    2. From the config file create host and connect to target.
    3. Delete Host.
    4. Delete Target.
"""


import sys
from nose.tools import assert_equal
sys.path.append("../")
# from nvmf.misc.null_blk import NullBlk
from nvmf.misc.loopback import Loopback
from nvmf_test import NVMFTest
from nvmf.target import NVMFTarget
from nvmf.host import NVMFHost


class TestNVMFCreateHost(NVMFTest):

    """ Represents Host Creation testcase """

    def __init__(self):
        NVMFTest.__init__(self)
        self.host_subsys = None
        self.target_subsys = None
        self.setup_log_dir(self.__class__.__name__)

    def setUp(self):
        """ Pre section of testcase """
        self.loopdev = Loopback(self.mount_path, self.data_size,
                                self.block_size, self.nr_dev)
        self.loopdev.init()
        self.build_target_config(self.loopdev.dev_list)
        self.target_subsys = NVMFTarget(self.target_type)
        ret = self.target_subsys.config(self.target_config_file)
        assert_equal(ret, True, "ERROR : target config failed")
        self.host_subsys = NVMFHost(self.target_type)

    def tearDown(self):
        """ Post section of testcase """
        self.host_subsys.delete()
        self.target_subsys.delete()
        self.loopdev.delete()

    def test_create_host(self):
        """ Testcase main """
        print("Now Running " + self.__class__.__name__)
        ret = self.host_subsys.config(self.target_config_file)
        assert_equal(ret, True, "ERROR : host config failed")
        raw_input("Press enter to continue ...")
