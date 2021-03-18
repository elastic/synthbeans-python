# -*- coding: utf-8 -*-
import argparse
import synthbean
import asyncio
from halo import Halo

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ac-dc', action="store_true")

    cli_args = parser.parse_args()
    apm_config = synthbean.render_apm_config()

    synth_config = synthbean.render_synth_config()
    loop = asyncio.get_event_loop()

    num_workers = synth_config.get('instance_count', 1)
    for i in range(0, num_workers):
        client = synthbean.apm_preflight(
            apm_config['elasticapm'],
            f"synthbean-python-{str(i)}",
            synth_config
            )
        synthbean.create_span_pool(synth_config, loop, client)

    welcome_text = 'SynthBean active!'

    if cli_args.ac_dc: 
        synthbean.create_easter()
        welcome_text = '-- 🎸🏴‍☠️️ For those who about to rock, the Elastic Observability Team salutes you! --'

    with Halo(text=welcome_text, spinner='dots') as spinner:
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            spinner.info('SynthBean finished!')

    tasks = asyncio.all_tasks(loop=loop)

    for t in tasks:
        t.cancel()

    group = asyncio.gather(*tasks, return_exceptions=True)

    loop.run_until_complete(group)
    loop.close()
