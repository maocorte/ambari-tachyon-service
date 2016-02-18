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
import os, hashlib
from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File, Execute, Directory


class Tachyon(Script):

  def base_install(self, env):
    import params

    self.install_packages(env)

    if not os.path.exists(params.base_dir):

      if not os.path.exists(params.tachyon_tmp_file):
        Execute(
            'wget '+params.tachyon_download_link+' -O '+params.tachyon_tmp_file+' -a /tmp/tachyon_download.log',
            user=params.tachyon_user
        )
      else:
        hadoop_tmp_file_md5 = hashlib.md5(open(params.tachyon_tmp_file, "rb").read()).hexdigest()

        if not hadoop_tmp_file_md5 == params.binary_file_md5:
          Execute(
              'rm -f '+params.tachyon_tmp_file,
              user=params.tachyon_user
          )

          Execute(
              'wget '+params.tachyon_download_link+' -O '+params.tachyon_tmp_file+' -a /tmp/tachyon_download.log',
              user=params.tachyon_user
          )

      if not os.path.isfile('/etc/sudoers.pre_tachyon.bak'):
        Execute('cp /etc/sudoers /etc/sudoers.pre_tachyon.bak')
        Execute('echo "'+params.tachyon_user+'    ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers')


      Directory(
          [params.base_dir, params.underfs_addr, params.pid_dir, params.log_dir],
          owner=params.tachyon_user,
          group=params.user_group,
          recursive=True
      )

      Execute(
          '/bin/tar -zxf ' + params.tachyon_tmp_file + ' --strip 1 -C ' + params.base_dir,
          user=params.tachyon_user
      )

  def configure(self, env):
    import params

    env.set_params(params)

    tachyon_config_dir = params.base_dir + '/conf'
    tachyon_libexec_dir = params.base_dir + '/libexec'

    File(
        format("{tachyon_config_dir}/tachyon-env.sh"),
        owner=params.tachyon_user,
        mode=0700,
        content=Template('tachyon-env.sh.j2', conf_dir=tachyon_config_dir)
    )

    File(
        format("{tachyon_config_dir}/workers"),
        owner=params.tachyon_user,
        mode=0644,
        content='\n'.join(params.tachyon_workers)
    )

    File(
        format("{tachyon_libexec_dir}/tachyon-config.sh"),
        owner=params.tachyon_user,
        mode=0700,
        content=Template('tachyon-config.sh.j2', conf_dir=tachyon_libexec_dir)
    )

  def stop(self, env, node_type):
    import params

    cmd = params.base_dir + '/bin/tachyon-stop.sh ' + node_type

    Execute('echo "Running cmd: ' + cmd + '"')
    Execute(cmd, user='root')