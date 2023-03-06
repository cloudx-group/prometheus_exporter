<h1 align="left">About</h1>
Prometheus_exporter tool is a collector and exporter of the JMX metrics in Prometheus.
The exporter listens to the mBeans JMX Hadoop metrics, collects, transforms and exports Prometheus metrics on the local host.

## How to run

->  prometheus_exporter git:(master) ✗ python3 -m pip install -r requirements.txt

->  use .\src\configs\config.yaml for configurate your exporter params (logging and etc...)

->  run python3 prometheus_exporter.py -h
    usage: prometheus_exporter.py [-h] -cluster cluster_name
                                [-queue yarn_queue_regexp]
                                [-ns [node_jmx_url [node_jmx_url ...]]]                              
                                [-rms [resourcemanager_jmx_url [resourcemanager_jmx_url ...]]]
                                [-jns [journalnode_jmx_url [journalnode_jmx_url ...]]]
                                [-host host]
                                [-port port]



*Optional arguments:*
```
-h, --help								Show this help message and exit
-cluster cluster_name						        Hadoop cluster name (can be HA name)
-queue yarn_queue_regexp						Regular expression of queue name. default: root.*
-ns [node_jmx_url [node_jmx_url ...]]					Hadoop hdfs cluster nodes jmx metrics URL.
-rms [resourcemanager_jmx_url [resourcemanager_jmx_url ...]]	        Hadoop resourcemanager metrics jmx URL.
-jns [journalnode_jmx_url [journalnode_jmx_url ...]]			Hadoop journalnode jmx metrics URL.
-host host								Listen on this address. default: 0.0.0.0
-port port								Listen to this port. default: 6688
```

*For example:*
```
python3 prometheus_exporter.py -cluster yh-cdh -nns http://10.193.40.10:50070/jmx http://10.193.40.3:50070/jmx -rms http://yh-shhd-cdh04:8088/jmx http://yh-shhd-cdh01:8088/jmx
```

Listen at 0.0.0.0:6688 or open your browser to view metrics: http://127.0.0.1:6688/metrics

![Dashboard screenshot](https://github.com/cloudx-group/prometheus_exporter/blob/1f594bf9103d1cafdfc1093cbf3aee3d0336d83d/src/docs/HDFS-NameNode.png)