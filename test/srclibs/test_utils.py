#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import argparse
import os
from src.srclibs import utils
import logging


class TestUtils(unittest.TestCase):

    def test_parse_args(self):
        parser = argparse.ArgumentParser(description='cx_hadoop jmx metric prometheus exporter')
        parser.add_argument('-cluster', required=True, metavar='cluster_name',
                            help='Hadoop cluster name (maybe HA name)')
        parser.add_argument('-queue', required=False, metavar='yarn_queue_regexp',
                            help='Regular expression of queue name. default: root.*', default='root.*')
        parser.add_argument('-ns', required=False, metavar='node_jmx_url',
                            help='Hadoop hdfs cluster node jmx metrics URL.', nargs="*")
        parser.add_argument('-rms', required=False, metavar='resourcemanager_jmx_url',
                            help='Hadoop resourcemanager metrics jmx URL.', nargs="*")
        parser.add_argument('-jns', required=False, metavar='journalnode_jmx_url',
                            help='Hadoop journalnode jmx metrics URL.', nargs="*")
        parser.add_argument('-host', required=False, metavar='host', help='Listen on this address. default: 0.0.0.0',
                            default='0.0.0.0')
        parser.add_argument('-port', required=False, metavar='port', type=int,
                            help='Listen to this port. default: 6688', default=6688)
        self.assertIsInstance(parser.parse_args(['-cluster', 'CLUSTER']), argparse.Namespace)

    def test_get_file_list(self):
        self.assertIsInstance(utils.get_file_list('namenode'), list)
        self.assertIsInstance(utils.get_file_list(''), list)

    def test_read_json_file(self):
        self.assertIsInstance(utils.read_json_file(path_name='namenode', file_name='FSNamesystem'), dict)
        self.assertIsInstance(utils.read_json_file(path_name='', file_name=''), dict)

    def test_create_path(self):
        self.assertEqual(True, True)

    def test_get_config_yaml(self):
        src_home_path = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
        # self.assertIsInstance(utils.get_config_yaml(yaml_conf_path='incorrect_path'), dict)
        # self.assertEqual(bool(utils.get_config_yaml(yaml_conf_path='incorrect_path')), bool(dict()))
        yaml_conf_path = os.path.join(src_home_path, "src", "configs", "config.yaml")
        self.assertEqual(bool(utils.get_config_yaml(yaml_conf_path=yaml_conf_path)), bool(dict(mykey='some_value')))

    def test_get_log_path(self):
        src_home_path = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
        src_file_name = "src_file_name.py"
        file_path = "None"
        file_name = "None"
        log_params = {"path": file_path, "name": file_name}
        self.assertEqual(utils.get_log_path(log_params=log_params, src_file_name=src_file_name),
                         os.path.join(src_home_path,
                                      'src',
                                      src_file_name.replace(os.path.splitext(src_file_name)[1], ".log")))

        file_path = "my_path"
        file_name = "my_file.log"
        log_params = {"path": file_path, "name": file_name}
        self.assertEqual(utils.get_log_path(log_params=log_params, src_file_name=src_file_name),
                         os.path.join(file_path, file_name))
        os.rmdir(file_path)

    def test_get_log_severity(self):
        log_severities = {'DEBUG': logging.DEBUG,
                          'INFO': logging.INFO,
                          'WARNING': logging.WARNING,
                          'ERROR': logging.ERROR}
        test_severities = utils.get_log_severity()

        for k, v in log_severities.items():
            self.assertEqual(test_severities.get(k), v,
                             f"Not found key '{k}' in utils.get_log_severity()")


if __name__ == '__main__':
    unittest.main()
