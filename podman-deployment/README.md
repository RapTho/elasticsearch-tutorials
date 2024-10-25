# Deploy Elasticsearch + Kibana using Podman Compose

## Install podman and podman compose

Podman is like Docker but it doesn't require root privileges ;)<br>

If you want, you can later set an alias to run docker commands, which will actually be executed by podman. that's how similar the two are

```bash
alias docker=podman
```

Install podman: [https://podman.io/docs/installation](https://podman.io/docs/installation)<br>
Install podman compose: [https://github.com/containers/podman-compose?tab=readme-ov-file#installation](https://github.com/containers/podman-compose?tab=readme-ov-file#installation)

## Deploy Elasticsearch + Kibana

Instructions: [https://www.elastic.co/guide/en/elasticsearch/reference/8.15/docker.html#docker-compose-file](https://www.elastic.co/guide/en/elasticsearch/reference/8.15/docker.html#docker-compose-file)

Check the cluster's health from the command line

```bash
curl -k -u "elastic:${ELASTIC_PASSWORD}" https://localhost:9200/_cluster/health
```

-k = skip TLS validation<br>
-u = provide username:password

## Open Kibana

Open a browser and visit [http://localhost:5601](http://localhost:5601)

### Troubleshoot

#### Sneaky way

Set `bootstrap.memory_lock=false` in your [docker-compose.yml](./docker-compose.yml) file to skip bootstrap checks. This is of course you'd do in production!

```bash
bootstrap.memory_lock=false
```

#### Set required node settings

In production you of course want to run the bootstrap checks to ensure your node is configured properly. Here you find the important settings that must be set:<br>
[https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html)
