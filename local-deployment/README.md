# Deploy Elasticsearch + Kibana using Podman Compose

## Install podman

[Podman](https://podman.io) is like Docker but it doesn't require root privileges ;)<br>

Install podman desktop: [https://podman-desktop.io/](https://podman-desktop.io/)<br>

Make sure [compose is setup](https://podman-desktop.io/docs/compose/setting-up-compose) and [Docker compatibility is enabled](https://podman-desktop.io/docs/migrating-from-docker/managing-docker-compatibility).

## Deploy Elasticsearch + Kibana

Instructions: [https://www.elastic.co/guide/en/elasticsearch/reference/8.15/docker.html#docker-compose-file](https://www.elastic.co/guide/en/elasticsearch/reference/8.15/docker.html#docker-compose-file)

The default username is `elastic`

Check the cluster's health from the command line

```bash
curl -k -u "elastic:${ELASTIC_PASSWORD}" https://localhost:9200/_cluster/health
```

-k = skip TLS validation<br>
-u = provide username:password

## Open Kibana

Open a browser and visit [http://localhost:5601](http://localhost:5601)

### Troubleshoot

Your cluster might fail to start due to failing bootstrap checks. Find the following workarounds below.

#### Sneaky way

Set `bootstrap.memory_lock=false` in your [docker-compose.yml](./docker-compose.yml) file to skip this bootstrap checks. This is of course nothing you'd do in production!

```bash
bootstrap.memory_lock=false
```

#### Set required node settings

In production you would want to run the bootstrap checks to ensure your node is configured properly. Here you find the important settings that must be set:<br>
[https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html)
