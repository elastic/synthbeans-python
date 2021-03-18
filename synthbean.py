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
import synthbean
import synthbean.config
import asyncio
from halo import Halo

if __name__ == '__main__':
    cli_args = synthbean.config.gather_args()
    welcome_text = synthbean.gen_welcome_msg(cli_args)

    apm_config = synthbean.config.render_apm_config()
    synth_config = synthbean.config.render_synth_config()

    loop = asyncio.get_event_loop()

    num_workers = synth_config.get('instance_count', 1)
    stack_config = apm_config['elasticapm']

    if synth_config.get('spans'):
        for i in range(0, num_workers):
            client = synthbean.apm_preflight(
                stack_config,
                synthbean.gen_instance_name(i),
                synth_config
            )
            synthbean.create_span_pool(synth_config, loop, client)

    if synth_config.get('instances'):
        for instance_name in synth_config['instances']:
            client = synthbean.apm_preflight(
                stack_config,
                instance_name,
                synth_config 
            )

            synthbean.create_span_pool(
                synth_config['instances'][instance_name],
                loop,
                client
            )

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
