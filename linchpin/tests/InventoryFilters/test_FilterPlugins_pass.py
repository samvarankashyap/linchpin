#!/usr/bin/env python

# flake8: noqa

from __future__ import absolute_import
import os
import json
import yaml

from nose.tools import *
import linchpin.FilterUtils.FilterUtils as filter_utils


def test_add_res_type():
    hosts = [{}]
    new_hosts = filter_utils.add_res_type(hosts, "test_res_type")
    assert_equal("test_res_type", new_hosts[0].get("resource_type"))


def test_fetch_attr():
    test_dict = { "a": "b" }
    assert_equal("b", filter_utils.fetch_attr(test_dict, "a", "c"))
    assert_equal("d", filter_utils.fetch_attr(test_dict, "d", "d"))


def test_format_output():
    assert_equal("{}", filter_utils.format_output({}))

def test_provide_default_omit():
    assert_equal("omit", filter_utils.provide_default("", "omit"))

def test_provide_default_val():
    assert_equal("a", filter_utils.provide_default("a", "omit"))

"""
def get_pod_status(pod_list, res_def_out):
    # this filter runs only when the kind is "Pod"
    pod_status = pod_list.get("resources", [])
    pod_stats = {}
    # filters out all the pods data w.r.to containers
    # provisioned in pods
    for x in pod_status:
        if x["metadata"]["name"] == res_def_out["result"]["metadata"]["name"]:
            pod_data = x
            pod_data["status"] = x["status"]["phase"]
            pod_stats[x["metadata"]["name"]] = pod_data
    # checks for the status of the pod and returns Failure value
    # when any pod is not in Running state
    for name in pod_stats.keys():
        if pod_stats[name]["status"] != "Running":
            return "Failure"
    return pod_stats
"""

def test_get_pod_status():
    assert_equal({}, filter_utils.get_pod_status({}, {}))


def test_get_pod_status_failure():
#    assert_equal({}, filter_utils.get_pod_status({}, {}))
    pass

def test_format_rules():
    rules = [{"rule_type": "inbound",
              "from_port": 22,
              "to_port": 22,
              "cidr_ip": "10",
              "proto": "tcp"
              }]
    expected = [{
              "from_port": 22,
              "to_port": 22,
              "cidr_ip": "10",
              "proto": "tcp"
               }]

    assert_equal(expected, filter_utils.format_rules(rules, "inbound"))

def test_fetch_list_by_attr():
    output = [{"a": "b"}, {"c","d"} ]
    assert_equal(["b"], filter_utils.fetch_list_by_attr(output, "a"))

def test_get_host_from_uri():
    test_str = "qemu+ssh://192.168.122.6/system"
    assert_equal("192.168.122.6", filter_utils.get_host_from_uri(test_str))

def test_get_host_from_uri_local():
    assert_equal("localhost", filter_utils.get_host_from_uri("test:///default"))

def test_get_provider_resources():
    test_out = [{"resource_type": "openstack"}]
    assert_equal(test_out,
                 filter_utils.get_provider_resources(test_out,
                                                     "openstack"))

def test_format_networks():
    networks = ["test"]
    assert_equal("net-name=test", filter_utils.format_networks(networks))

def test_os_server_insts():
    res_def = { "count": 2 }
    expected = [{ "name": "testname1"}, {"name": "testname2" }]
    assert_equals(expected, filter_utils.render_os_server_insts(res_def, "testname"))

def test_merge_two_dicts():
    a = { "a": "b" }
    b = { "b": "c" }
    expected = {"a": "b", "b": "c"}
    assert_equals(expected, filter_utils.merge_two_dicts(a, b))

def test_combine_hosts_name():
    hosts = [{"a": "b"}, {"d": "e"}]
    names = [{"c": "d"}]
    expected = [{'a': 'b', 'c': 'd'}, {'d': 'e'}]
    assert_equals(expected, filter_utils.combine_hosts_names(hosts, names))

def test_filter_list_by_attr():
    output = [{"a": "b"}, {"d": "e"}]
    attr = "a"
    expected = [{"a":"b"}]
    assert_equals(expected, filter_utils.filter_list_by_attr(output, attr))

def test_translate_ruletype_inbound():
    assert_equals("ingress", filter_utils.translate_ruletype("inbound"))


def test_translate_ruletype_inbound():
    assert_equals("egress", filter_utils.translate_ruletype("outbound"))

def test_translate_ruletype_invalid():
    assert_equals("invalid ruletype ", filter_utils.translate_ruletype("x"))

def test_filter_list_by_attr_val():
    test_list = [{"a":"b"}, {"c":"d"}]
    expected = [{"a": "b"}]
    assert_equals(expected, 
                  filter_utils.filter_list_by_attr_val(test_list, "a", "b"))

def test_map_results():
    test = [{ "a": {"b": "c"} }]
    assert_equals(["c"], filter_utils.map_results(test, "a", "b"))

def test_prepare_ssh_args():
    ssh_args = ""
    users = ["testuser"]
    sshkey = "xyz"
    assert_equals("--ssh-inject testuser:string:'xyz' ",
                  filter_utils.prepare_ssh_args("",users, sshkey))

def test_transform_os_server_output():
    res_def_out = {"results": [{ "id": "testid" }]}
    expected = {'ids': ['testid'], 'openstack': [{}], 'servers': [{}]}
    assert_equals(expected, filter_utils.transform_os_server_output(res_def_out))