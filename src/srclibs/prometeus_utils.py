#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from prometheus_async.aio import web as prom_web
from prometheus_client.core import REGISTRY

from src.srclibs.hdfs_namenode import NameNodeMetricCollector
from src.srclibs.hdfs_datanode import DataNodeMetricCollector
from src.srclibs.hdfs_journalnode import JournalNodeMetricCollector
from src.srclibs.yarn_resourcemanager import ResourceManagerMetricCollector
from src.srclibs.yarn_nodemanager import NodeManagerMetricCollector


class PrometheusClientWebServer(object):
    obj_metrics_server = None
    obj_counter = None

    async def server_start(self, args):
        print("Starting prometheus server...")
        logging.info("Starting prometheus server...")
        self.obj_metrics_server = await prom_web.start_http_server(addr=args.host,
                                                                   port=int(args.port))
        print("Listen at %s:%s" % (args.host, int(args.port)))
        self.register_prometheus(args.cluster, args=args)
        print("Starting prometheus server - DONE")
        logging.info("Starting prometheus server - DONE")

    def register_prometheus(self, cluster, args):
        if args.ns is not None and len(args.ns) > 0:
            nc = NameNodeMetricCollector(cluster, args.ns)
            nc.collect()
            REGISTRY.register(nc)
            REGISTRY.register(DataNodeMetricCollector(cluster, nc))
        if args.rms is not None and len(args.rms) > 0:
            rmc = ResourceManagerMetricCollector(cluster, args.rms, args.queue)
            rmc.collect()
            REGISTRY.register(rmc)
            REGISTRY.register(NodeManagerMetricCollector(cluster, rmc))
        if args.jns is not None and len(args.jns) > 0:
            REGISTRY.register(JournalNodeMetricCollector(cluster, args.jns))
