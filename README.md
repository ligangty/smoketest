# Smoke test environment for indy clustering with auditquery

## Pre-requision
  * java  
  * git
  * mvn
  * docker 
  * docker-compose

## Steps
  * Change jgroups gossip: in both auditquery/conf/jgroups-tcp.xml and indy/etc/indy/jgroups-tcp.xml, find "<TUNNEL gossip_router_hosts="0.0.0.0[12001]" />" and replace the ip "0.0.0.0" to your local ip.
  * Run prepare.sh: will download two projects and build, then use prepared docker build env to build docker file and start these two built images through docker-compose. In the meantime, a jboss/gossip jgroup node will also be started as intermediate communication node between ispn cluster nodes.
  * Access both localhost:8080 for indy and localhost:8082 for auditquery, and test repository change log features
  
