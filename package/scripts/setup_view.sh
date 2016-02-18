#!/bin/sh
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

set -e

export INSTALL_DIR=$1
export TACHYON_MASTER_HOST=$2
export AMBARI_SERVER_HOST=$3

echo "Setting up zeppelin at $INSTALL_DIR"
cd $INSTALL_DIR

if [ -d ambari-iframe-view ]
then
    rm -rf ambari-iframe-view
fi
if [ -d tachyon-view ]
then
    rm -rf tachyon-view
fi

git clone https://github.com/radicalbit/ambari-iframe-view.git

rm -rf ambari-iframe-view/samples
rm -rf ambari-iframe-view/screenshots
rm -f ambari-iframe-view/README.md



sed -i "s/iFrame View/Tachyon/g" ambari-iframe-view/src/main/resources/view.xml
sed -i "s/IFRAME_VIEW/TACHYON/g" ambari-iframe-view/src/main/resources/view.xml
sed -i "s/sandbox.hortonworks.com:6080/$TACHYON_MASTER_HOST:19999/g" ambari-iframe-view/src/main/resources/index.html
sed -i "s/iframe-view/tachyon-view/g" ambari-iframe-view/pom.xml
sed -i "s/Ambari iFrame View/Tachyon View/g" ambari-iframe-view/pom.xml

mv ambari-iframe-view tachyon-view

cd tachyon-view
mvn clean package

scp target/*.jar "$AMBARI_SERVER_HOST:/var/lib/ambari-server/resources/views"

cd ..
rm -rf tachyon-view