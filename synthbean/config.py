# -*- coding: utf-8 -*-
# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import os
import argparse
import yaml
import configparser


def gather_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ac-dc', action="store_true")
    return parser.parse_args()


def render_apm_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('conf/settings.ini')

    server_url_env = os.environ.get('SYNTHBEAN_SERVER_URL')
    if server_url_env: 
        config['elasticapm']['server_url'] = server_url_env

    service_name_env = os.environ.get('SYNTHBEAN_SERVICE_NAME') 
    if service_name_env:
       config['elasticapm']['service_name'] = service_name_env

    log_level_env = os.environ.get('SYNTHBEAN_LOG_LEVEL')
    if log_level_env:
        config['elasticapm']['log_level'] = log_level_env

    
    environment_env = os.environ.get('SYNTHBEAN_ENVIRONMENT')
    if environment_env:
        config['elasticapm']['environment'] = environment_env

    cloud_provider_env = os.environ.get('SYNTHBEAN_CLOUD_PROVIDER')
    if cloud_provider_env:
        config['elasticapm']['cloud_provider'] = cloud_provider_env
    
    return config


def render_synth_config() -> dict:
    with open("conf/synthbean.yml") as fh_:
        synth_config = yaml.load(fh_, Loader=yaml.FullLoader)
    return synth_config
