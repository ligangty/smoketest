FROM jboss/base-jdk:8

# configuration dir
#ENV INDY_ETC_DIR /usr/share/indy/etc

LABEL maintainer="NOS <nos-devel@redhat.com>" 

USER root

# NCL-2855: All services should run with UTC timezone
ENV TZ UTC

EXPOSE 8080 8081

COPY pkg/indy.tar.gz /tmp/indy.tar.gz

RUN tar -zxf /tmp/indy.tar.gz -C /opt && rm /tmp/indy.tar.gz

COPY etc/indy/conf.d/infinispan-cluster.conf /opt/indy/etc/indy/conf.d/infinispan-cluster.conf
COPY etc/indy/conf.d/repo-changelog.conf /opt/indy/etc/indy/conf.d/repo-changelog.conf
COPY etc/indy/infinispan-cluster.xml /opt/indy/etc/indy/infinispan-cluster.xml
COPY etc/indy/jgroups-tcp.xml /opt/indy/etc/indy/jgroups-tcp.xml

ENTRYPOINT ["/opt/indy/bin/indy.sh"]