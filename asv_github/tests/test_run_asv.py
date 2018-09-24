# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import random
import string
import tempfile
from unittest import mock

from asv_github import run_asv
from asv_github.tests import base


def choices(num):
    out = ''
    for i in range(num):
        out += ''.join(random.choice(string.ascii_uppercase))
    return out


class TestRunAsv(base.TestCase):

    @mock.patch('subprocess.call')
    def test_asv_run_all(self, subprocess_mock):
        run_asv.asv_run_all('/tmp')
        subprocess_mock.assert_called_once_with(['asv', 'run', '-e',
                                                 '--launch-method=spawn',
                                                 'ALL'], cwd='/tmp')

    @mock.patch('subprocess.call')
    def test_asv_run_new(self, subprocess_mock):
        run_asv.asv_run_new('/tmp')
        subprocess_mock.assert_called_once_with(['asv', 'run', '-e',
                                                 '--launch-method=spawn',
                                                 'NEW'], cwd='/tmp')

    @mock.patch('subprocess.call')
    def test_asv_publish(self, subprocess_mock):
        run_asv.asv_publish('/tmp', '/out')
        subprocess_mock.assert_called_once_with(['asv', 'publish',
                                                 '--html-dir',
                                                 '/out'], cwd='/tmp')

    def test_invalid_dir_asv_run(self):
        temp_path = tempfile.gettempdir()
        fake_working_dir = choices(7)
        test_path = os.path.join(temp_path, fake_working_dir)
        self.assertRaises(FileNotFoundError, run_asv.asv_run_all, test_path)

    def test_invalid_dir_asv_new(self):
        temp_path = tempfile.gettempdir()
        fake_working_dir = choices(7)
        test_path = os.path.join(temp_path, fake_working_dir)
        self.assertRaises(FileNotFoundError, run_asv.asv_run_new, test_path)

    def test_invalid_dir_asv_publish(self):
        temp_path = tempfile.gettempdir()
        fake_working_dir = choices(7)
        test_path = os.path.join(temp_path, fake_working_dir)
        self.assertRaises(FileNotFoundError, run_asv.asv_publish, test_path,
                          '/out')
