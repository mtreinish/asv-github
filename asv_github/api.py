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

"""API server for running asv from github."""

import logging
import multiprocessing
import os
from urllib import parse

import flask
import github_webhook
import yaml

from asv_github import manage_git
from asv_github import run_asv

LOG = logging.getLogger(__name__)

APP = flask.Flask(__name__)
WEBHOOK = github_webhook.Webhook(APP)
ASV_MACHINE = False

REPOS = {}
CONFIG = None

ASV_QUEUE = multiprocessing.Queue()


def load_config():
    """Load config from file, else set defaults."""
    global CONFIG
    if os.path.isfile('/etc/asv-github-api.conf'):
        CONFIG = yaml.load('/etc/asv-github-api.conf')
        if 'git-dir' not in CONFIG['api']:
            LOG.warning(
                '"git-dir"not set in config file using default of "/tmp"')
            CONFIG['api']['git-dir'] = '/tmp'
        if 'html-dir' not in CONFIG['api']:
            LOG.warning(
                '"git-dir"not set in config file using default of '
                '"/var/www/html"')
            CONFIG['api']['html-dir'] = '/var/www/html'
    else:
        CONFIG = {
            'api': {
                'git-dir': '/tmp',
                'html-dir': '/var/www/html',
            }
        }


@APP.before_first_request
def _setup():
    setup()


def setup():
    """Setup config."""
    global CONFIG
    global ASV_QUEUE
    if not CONFIG:
        load_config()
    run_asv.ASVWorker(ASV_QUEUE, CONFIG['api']['html-dir']).start()


@APP.route("/", methods=['GET'])
def list_routes():
    """List routes on gets to root."""
    output = []
    for rule in APP.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        url = flask.url_for(rule.endpoint, **options)
        out_dict = {
            'name': rule.endpoint,
            'methods': sorted(rule.methods),
            'url': parse.unquote(url),
        }
        output.append(out_dict)
    return flask.jsonify({'routes': output})


def get_local_repo(name, git_url):
    """Handle creating a new local repo for benchmarking."""
    local_path = os.path.join(CONFIG['api']['git-dir'], name)
    REPOS[name] = manage_git.ASVRepo(local_path, git_url)
    return REPOS[name]


@WEBHOOK.hook()
def on_push(data):
    """Handle github WEBHOOK pushes."""

    global REPOS
    global ASV_MACHINE
    global ASV_QUEUE
    import pprint
    pprint.pprint(data)
#    data = json.loads(body)
    repo_name = data['repository']['full_name']
    git_url = data['repository']['git_url']
    if repo_name not in REPOS:
        local_repo = get_local_repo(repo_name, git_url)
        local_repo.clone_repo()
        if not ASV_MACHINE:
            run_asv.setup_machine(local_repo.local_path)
            ASV_MACHINE = True
    else:
        local_repo = REPOS[repo_name]
    ASV_QUEUE.put(local_repo)


def main():
    """Run APP."""
    APP.run(debug=True, host='127.0.0.1', port=80)

if __name__ == "__main__":
    main()
