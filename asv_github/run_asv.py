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

import subprocess

import multiprocessing


class ASVWorker(multiprocessing.Process):

    def __init__(self, queue, html_dir):
        self.queue = queue
        self.html_dir = html_dir

    def run(self):
        while True:
            repo = self.queue.get()
            cwd = repo.local_path
            repo.repo.pull()
            asv_run_new(cwd)
            asv_publish(cwd)


def asv_publish(cwd, html_dir):
    cmd = ['asv', 'publish', '--html-dir', html_dir]
    subprocess.call(cmd, cwd=cwd)


def _asv_run(commits, cwd):
    cmd = ['asv', 'run', '-e', '--launch-method=spawn', commits]
    subprocess.call(cmd, cwd=cwd)


def asv_run_new(cwd):
    _asv_run('NEW', cwd)


def setup_machine(cwd, name=None, os=None, arch=None, cpu=None, ram=None):
    cmd = ['asv', 'machine']
    if not name and not os and not arch and not cpu and not ram:
        cmd.append('--yes')
    else:
        if name:
            cmd += ['--machine', name]
        if os:
            cmd += ['--os', os]
        if arch:
            cmd += ['--arch', arch]
        if cpu:
            cmd += ['--cpu', cpu]
        if ram:
            cmd += ['--ram', ram]
    subprocess.call(cmd, cwd=cwd)
