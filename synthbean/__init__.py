# -*- coding: utf-8 -*-
import yaml
import random
import asyncio
import configparser
import elasticapm

def render_apm_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('conf/settings.ini')
    return config

def render_synth_config() -> dict:
    with open("conf/synthbean.yml") as fh_:
        synth_config = yaml.load(fh_, Loader=yaml.FullLoader)
    return synth_config

def apm_preflight(config, node_name, synth_config) -> elasticapm.Client:

    # We're being a bit naughty here. Shhhh.
    elasticapm.utils.cgroup.get_cgroup_container_metadata = lambda: {'container': {'id': node_name}}
    processors = []
    if synth_config.get('smoothing_strategy') == 'floor':
        for span in synth_config['spans']:
            if synth_config['spans'][span].get('jitter'):
                raise Exception('Cannot use jitter and the "floor" smoothing strategy concurrently')
        processors.append('synthbean.processors.span_smoother')


    client = elasticapm.Client(
        hostname=node_name,
        service_node_name=node_name,
        service_name=config['service_name'],
        server_url=config['server_url'],
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
    for span in synth_config['spans']:
        async def worker(delay, span, jitter):
             while True:
                if jitter:
                    delay = calculate_jitter(delay, jitter)
                client.begin_transaction(transaction_type="script")
                await asyncio.sleep(delay / 1000)
                client.end_transaction(name=span, result="success")

        span_config = synth_config['spans'][span]
        loop.create_task(worker(span_config['duration'], span, span_config.get('jitter')))

def create_easter() -> None:
    import synthbean.resources.easter
    from multiprocessing import Process
    p = Process(target=synthbean.resources.easter.easter_time)
    p.start()
