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

from unittest import mock

from asv_github import manage_git
from asv_github.tests import base


class TestManageGit(base.TestCase):

    @mock.patch('subprocess.call')
    def test_clone(self, subprocess_mock):
        repo = manage_git.ASVRepo('/tmp', 'git://fake-repo.org')
        repo.clone_repo()
        subprocess_mock.assert_called_once_with(['git', 'clone',
                                                 'git://fake-repo.org',
                                                 '/tmp'])

    @mock.patch('os.path.isdir', return_value=True)
    def test_clone_already_exists(self, is_dir_mock):
        repo = manage_git.ASVRepo('/tmp', 'git://fake-repo.org')
        self.assertRaises(OSError, repo.clone_repo)
        is_dir_mock.assert_called_once_with('/tmp/.git')
