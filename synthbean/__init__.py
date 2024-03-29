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
import random
import asyncio
import elasticapm
import elasticapm.utils.cgroup

def gen_instance_name(instance_num: int) -> str:
    return f"synthbean-python-{str(instance_num)}"


def gen_welcome_msg(cli_args):
    welcome_text = 'SynthBean active!'
    if cli_args.ac_dc:
        create_easter()
        welcome_text = '-- 🎸🏴‍☠️️ For those who are about to rock, the Elastic Observability Team salutes you! --'
    return welcome_text

def verify_smoothing_config(synth_config):
    if synth_config.get('smoothing_strategy') == 'floor' and synth_config.get('transactions'):
        for transaction in synth_config['transactions']:
            if synth_config['transactions'][transaction].get('jitter'):
                raise Exception(
                    'Cannot use jitter and the "floor" smoothing strategy concurrently')


def apm_preflight(stack_config, node_name, synth_config) -> elasticapm.Client:

    verify_smoothing_config(synth_config)

    # We're being a bit naughty here. Shhhh.
    elasticapm.utils.cgroup.get_cgroup_container_metadata = lambda: {
        'container': {'id': node_name}}

    processors = []

    if synth_config.get('smoothing_strategy') == 'floor':
        processors.append('synthbean.processors.span_smoother')

    client = elasticapm.Client(
        hostname=node_name,
        service_node_name=node_name,
        service_name=stack_config['service_name'],
        server_url=stack_config['server_url'],
        processors=processors)

    elasticapm.instrument()
    return client


def calculate_jitter(delay: int, jitter: int) -> int:
    jitter_val = random.randint(0, jitter)
    if jitter_val % 2:
        delay += jitter_val
    else:
        delay -= jitter_val
    return delay


def create_span_pool(synth_config, loop, client) -> None:
    for transaction in synth_config['transactions']:
        async def worker(delay, transaction, jitter):
            while True:
                if jitter:
                    delay = calculate_jitter(delay, jitter)
                client.begin_transaction(transaction_type="script")
                await asyncio.sleep(delay / 1000)
                client.end_transaction(name=transaction, result="success")

        transaction_config = synth_config['transactions'][transaction]
        loop.create_task(
            worker(transaction_config['duration'], transaction, transaction_config.get('jitter')))


def create_easter() -> None:
    import synthbean.resources.easter
    from multiprocessing import Process
    p1 = Process(target=synthbean.resources.easter.easter_time)
    p1.start()

    p2 = Process(target=synthbean.resources.easter.easter_show)
    p2.start()