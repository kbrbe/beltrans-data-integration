FROM lyrasis/blazegraph:2.1.5
ARG BLAZEGRAPH_GID=888
EXPOSE 8080
VOLUME /data

USER root
ENV BLAZEGRAPH_NAME=bigdata \
    BLAZEGRAPH_RW_PATH=/RWStore.properties \
    BLAZEGRAPH_VERSION=CANDIDATE_2_1_5 \
    JAVA_OPTS=$JAVA_OPTS \
    JETTY_WEBAPPS=/var/lib/jetty/webapps \
    BLAZEGRAPH_UID=1000 \
    BLAZEGRAPH_GID=1000
# Create blazegraph user
ADD RWStore.properties /RWStore.properties 
RUN addgroup -S -g $BLAZEGRAPH_GID blazegraph
RUN adduser -S -s /bin/false -G blazegraph -u $BLAZEGRAPH_UID blazegraph

# Make sure permissions are good
RUN chown -R blazegraph:blazegraph "$JETTY_BASE" &&\
  chown -R blazegraph:blazegraph /RWStore.properties "$TMPDIR"
WORKDIR /var/lib/jetty
USER blazegraph

CMD java $JAVA_OPTS -Dcom.bigdata.rdf.sail.webapp.ConfigParams.propertyFile=/RWStore.properties -jar /usr/local/jetty/start.jar

