# Ambari Tachyon Service
Ambari service for installing and managing Tachyon on HDP clusters.
Tachyon is a memory-centric distributed storage system enabling reliable data sharing at memory-speed across cluster frameworks.

Author: [Mauro Cortellazzi](https://github.com/maocorte)

## Setup

- To download the Tachyon service folder, run below

```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo git clone https://github.com/maocorte/ambari-tachyon-service.git  /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/TACHYON   
```
- Restart Ambari

```
#sandbox
service ambari restart

#non sandbox
sudo service ambari-server restart
```

- Then you can click on 'Add Service' from the 'Actions' dropdown menu in the bottom left of the Ambari dashboard -> On bottom left -> Actions -> Add service -> check Tachyon -> Next -> check nodes to be present in the cluster-> Next -> Change any config you like -> Next -> Deploy
- On successful deployment you will see the Tachyon service as part of Ambari stack and will be able to start/stop the service
- You can see the parameters you configured under 'Configs' tab.

## Remove service

- To remove the Tachyon service:
  - Stop the service via Ambari
  - Unregister the service

```
export SERVICE=TACHYON
export PASSWORD=admin
export AMBARI_HOST=localhost
#detect name of cluster
output=`curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari'  http://$AMBARI_HOST:8080/api/v1/clusters`
CLUSTER=`echo $output | sed -n 's/.*"cluster_name" : "\([^\"]*\)".*/\1/p'`

curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X DELETE http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

#if above errors out, run below first to fully stop the service
#curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE
```
- Remove artifacts (check your configurations for your correct params, the script below is based on default values)

```
rm -rf /opt/tachyon
rm -rf /var/lib/tachyon
rm -rf /var/log/tachyon
rm -rf /var/run/tachyon
rm -rf /mnt/ramdisk

userdel -rf tachyon
```

## TODO

- Improve HA configuration with zookeeper