#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import yaml
import os


def parse_args():
    parser = argparse.ArgumentParser(description='hadoop jmx metric to prometheus exporter')
    parser.add_argument('-cluster', required=True, metavar='cluster_name', help='Hadoop cluster name (maybe HA name)')
    parser.add_argument('-queue',
                        required=False,
                        metavar='yarn_queue_regexp',
                        help='Regular expression of queue name. default: root.*',
                        default='root.*')
    parser.add_argument('-ns',
                        required=False,
                        metavar='node_jmx_url',
                        help='Hadoop hdfs cluster node jmx metrics URL.',
                        nargs="*")
    parser.add_argument('-rms',
                        required=False,
                        metavar='resourcemanager_jmx_url',
                        help='Hadoop resourcemanager metrics jmx URL.',
                        nargs="*")
    parser.add_argument('-jns',
                        required=False,
                        metavar='journalnode_jmx_url',
                        help='Hadoop journalnode jmx metrics URL.',
                        nargs="*")
    parser.add_argument('-host',
                        required=False,
                        metavar='host',
                        help='Listen on this address. default: 0.0.0.0',
                        default='0.0.0.0')
    parser.add_argument('-port',
                        required=False,
                        metavar='port',
                        type=int,
                        help='Listen to this port. default: 6688',
                        default=6688)
    return parser.parse_args()


# noinspection PyTypeChecker
def get_file_list(file_path_name):
    path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(path, "metrics", file_path_name)
    try:
        files = os.listdir(json_path)
    except OSError:
        logging.info("No such file or directory: '%s'" % json_path)
        return []
    else:
        rlt = []
        for i in range(len(files)):
            rlt.append(files[i].split(".json")[0])
        return rlt


def read_json_file(path_name, file_name):
    path = os.path.dirname(os.path.realpath(__file__))
    metric_path = os.path.join(path, "metrics", path_name)
    metric_name = "{0}.json".format(file_name)
    try:
        with open(os.path.join(metric_path, metric_name), 'r') as f:
            metrics = yaml.safe_load(f)
            return metrics
    except Exception as e:
        logging.info("read metrics json file failed, error msg is: %s" % e)
        return {}


def create_path(in_path):
    if os.path.isdir(in_path):
        return True
    else:
        try:
            os.makedirs(in_path)
            return True
        except Exception as e:
            print(f"ERROR MESSAGE: {e}")
            return False


def get_config_yaml(yaml_conf_path):
    try:
        if not os.path.isfile(yaml_conf_path):
            raise FileExistsError
        with open(yaml_conf_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: {e}")
        return {}
    except FileExistsError:
        print(f"ERROR: Couldn't found config.yaml")
        return {}


def get_log_path(log_params, src_file_name):

    if log_params.get("path").upper() == "NONE":
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    else:
        path = log_params.get("path")

    if not create_path(path):
        return None

    if log_params.get("name").upper() == "NONE":
        name = src_file_name.replace(os.path.splitext(src_file_name)[1], ".log")
    else:
        name = log_params.get("name")
    return os.path.join(path, name)


def get_log_severity():
    return {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }
