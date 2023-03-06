#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os

from src.srclibs import prometeus_utils as pu
from src.srclibs import utils


def main():

    args = utils.parse_args()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    obj_prom = pu.PrometheusClientWebServer()
    loop.run_until_complete(obj_prom.server_start(args=args))
    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        logging.error("There was KeyboardInterrupt")
        logging.error(f"Prometheus server was stopped")
        pass


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    yaml_conf_path = os.path.join(path, "src", "configs", "config.yaml")

    yaml_conf = utils.get_config_yaml(yaml_conf_path)
    if bool(yaml_conf):
        log_params = yaml_conf.get("log_param")
        if log_params.get("is_logging"):
            get_log_path = utils.get_log_path(log_params=log_params,
                                              src_file_name=os.path.basename(__file__))

            logging.basicConfig(filename=get_log_path,
                                level=utils.get_log_severity().get(log_params.get("logging_level")),
                                filemode='w',
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        else:
            print("INFO: Logging skipped")

        main()

    else:
        print("ERROR: cx_hadoop_exporter couldn't started")
