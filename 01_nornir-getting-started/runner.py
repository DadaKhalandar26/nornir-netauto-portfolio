"""
Nornir Getting Started - Basic Task Runner

This module demonstrates the fundamentals of Nornir:
  - Initializing Nornir from a config file
  - Loading inventory (hosts, groups, defaults)
  - Running a simple read-only task across multiple hosts in parallel
  - Inspecting results from all hosts

Key concepts:
  - AggregatedResult: Contains results from all hosts (dict-like, keyed by hostname)
  - MultiResult: Results for a single host's task chain (list of Result objects)
  - Result: Output from a single task execution

Author: Nornir Learning Track
Level: Basic
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command


nr = InitNornir(config_file='config.yaml')

run_result = nr.run(task=netmiko_send_command, command_string="sho ver")

for host, host_result in run_result.items():
    print(host)
    print(dir(host_result))
