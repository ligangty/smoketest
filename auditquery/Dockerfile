FROM jboss/base-jdk:8

# configuration dir
#ENV INDY_ETC_DIR /usr/share/indy/etc

LABEL maintainer="NOS <nos-devel@redhat.com>" 

USER root

# NCL-2855: All services should run with UTC timezone
ENV TZ UTC

EXPOSE 8081 8082

COPY pkg/auditquery.tar.gz /tmp/auditquery.tar.gz

RUN tar -zxf /tmp/auditquery.tar.gz -C /opt && rm /tmp/auditquery.tar.gz

COPY conf/infinispan-cluster.xml /opt/auditquery/conf/infinispan-cluster.xml
COPY conf/jgroups-tcp.xml /opt/auditquery/conf/jgroups-tcp.xml


ENTRYPOINT ["/opt/auditquery/bin/start.sh"]