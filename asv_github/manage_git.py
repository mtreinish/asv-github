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

import git

class ASVRepo:
    def __init__(self, local_path, source, repo):
        self.repo = repo
        self.source = source
        self.local_path = local_path


def clone_repo(source, local_dest):
    """Clone a repo."""
    repo = git.Git(local_dest)
    repo.clone(source)
    return ASVRepo(local_dest, source, repo)
