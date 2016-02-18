#!/usr/bin/config python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
#import os
from resource_management.libraries.script.script import Script

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

binary_file_md5 = 'a4ff1ffc9cdbf593ffb46839dec1bfbe'
tachyon_download_link = 'http://tachyon-project.org/downloads/files/0.8.2/tachyon-0.8.2-bin.tar.gz'
tachyon_tmp_file = '/tmp/tachyon-0.8.2-bin.tar.gz'

# tachyon underfs address
underfs_addr = config['configurations']['tachyon-config']['tachyon.underfs.address']

# tachyon worker memory alotment
worker_mem = config['configurations']['tachyon-config']['tachyon.worker.memory']

# tachyon log dir
log_dir = config['configurations']['tachyon-env']['tachyon.log.dir']

# tachyon pid dir
pid_dir = config['configurations']['tachyon-env']['tachyon.pid.dir']

# tachyon installation dir
base_dir = config['configurations']['tachyon-env']['tachyon.lib.dir']

tachyon_user = config['configurations']['tachyon-env']['tachyon_user']
user_group = config['configurations']['cluster-env']['user_group']

ambari_server = config['clusterHostInfo']['ambari_server_host']

# tachyon addresses

#tachyon_master = config['clusterHostInfo']['tachyon_master_hosts'][0]
if config['clusterHostInfo']['hostname'] in config['clusterHostInfo']['tachyon_master_hosts']:
  tachyon_master = config['clusterHostInfo']['hostname']
else:
  tachyon_master = config['clusterHostInfo']['tachyon_master_hosts'][0]

tachyon_workers = config['clusterHostInfo']['tachyon_slave_hosts']

# zookeeper infos
zookeeper_hosts = ''
if 'zookeeper_hosts' in config['clusterHostInfo']:
  zookeeper_hosts_list = config['clusterHostInfo']['zookeeper_hosts']
  if len(zookeeper_hosts_list) > 0:
      zookeeper_hosts = ':2181,'.join(zookeeper_hosts_list) + ':2181'

use_zookeeper = False
if zookeeper_hosts != '' and config['configurations']['tachyon-env']['tachyon.usezookeeper'] == 'True':
  use_zookeeper = True

