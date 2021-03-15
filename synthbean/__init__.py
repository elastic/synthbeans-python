import yaml
import asyncio
import configparser
import elasticapm

def render_apm_config():
    config = configparser.ConfigParser()
    config.read('conf/settings.ini')
    return config

def render_synth_config():
    with open("conf/synthbean.yml") as fh_:
        synth_config = yaml.load(fh_, Loader=yaml.FullLoader)
    return synth_config

def apm_preflight(config, node_name, smoothing_strategy):

    # We're being a bit naughty here. Shhhh.
    elasticapm.utils.cgroup.get_cgroup_container_metadata = lambda: {'container': {'id': node_name}}
    processors = []
    if smoothing_strategy == 'floor':
        processors.append('synthbean.processors.span_smoother')

    client = elasticapm.Client(
        hostname=node_name,
        service_node_name=node_name,
        service_name=config['service_name'],
        server_url=config['server_url'],
        processors=processors)
    
    elasticapm.instrument()
    return client

def create_span_pool(synth_config, loop, client):
    for span in synth_config['spans']:
        async def worker(delay, span):
             while True:
                client.begin_transaction(transaction_type="script")
                await asyncio.sleep(delay / 1000)
                client.end_transaction(name=span, result="success")
        loop.create_task(worker(synth_config['spans'][span]['duration'], span))