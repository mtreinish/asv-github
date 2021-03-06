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
import subprocess


class ASVRepo(object):
    def __init__(self, local_path, source):
        self.source = source
        self.local_path = local_path

    def clone_repo(self):
        """Clone a repo."""
        git_path = os.path.join(self.local_path, '.git')
        if os.path.isdir(git_path):
            raise OSError('Git repo already cloned')
        cmd = ['git', 'clone', self.source, self.local_path]
        subprocess.call(cmd)

    def pull(self):
        cmd = ['git', 'pull']
        subprocess.call(cmd, cwd=self.local_path)
