# Deploy Elasticsearch + Kibana using Docker / Podman Compose

## Install a container runtime

You can use either **Docker** or **Podman** to run this stack.

- **Docker Desktop** (Windows / macOS / Linux): [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- **Podman Desktop** (rootless alternative): [https://podman-desktop.io/](https://podman-desktop.io/)<br>
  Make sure [compose is set up](https://podman-desktop.io/docs/compose/setting-up-compose) and [Docker compatibility is enabled](https://podman-desktop.io/docs/migrating-from-docker/managing-docker-compatibility).

## Deploy Elasticsearch + Kibana

Full reference: [https://www.elastic.co/guide/en/elasticsearch/reference/8.15/docker.html#docker-compose-file](https://www.elastic.co/guide/en/elasticsearch/reference/8.15/docker.html#docker-compose-file)

### 1. Create your `.env` file

The compose file reads all passwords and settings from a `.env` file. Copy the example and edit the values:

**macOS / Linux**
```bash
cp .env.example .env
```

**Windows (PowerShell)**
```powershell
Copy-Item .env.example .env
```

Open `.env` in your editor and set at minimum:

| Variable | Description |
|----------|-------------|
| `STACK_VERSION` | Elastic Stack version (e.g. `8.15.0`) |
| `ELASTIC_PASSWORD` | Password for the `elastic` superuser |
| `KIBANA_PASSWORD` | Password for the internal `kibana_system` user |
| `MEM_LIMIT` | Memory limit per container in bytes (e.g. `1073741824` for 1 GB) |

### 2. Start the stack

**macOS / Linux / Windows (PowerShell)**
```bash
docker compose up -d
```

Or with Podman:
```bash
podman-compose up -d
```

### 3. Check cluster health

The default username is `elastic`.

**macOS / Linux**
```bash
curl -k -u "elastic:${ELASTIC_PASSWORD}" https://localhost:9200/_cluster/health
```

**Windows (PowerShell)**
```powershell
$password = $Env:ELASTIC_PASSWORD
curl.exe -k -u "elastic:$password" https://localhost:9200/_cluster/health
```

**Windows (CMD)**
```cmd
curl -k -u "elastic:%ELASTIC_PASSWORD%" https://localhost:9200/_cluster/health
```

Flags: `-k` skips TLS validation, `-u` provides `username:password`.

## Open Kibana

Open a browser and visit [http://localhost:5601](http://localhost:5601)

## Troubleshoot

### Docker Hub pull rate limits

Docker Hub applies pull rate limits based on IP address. Anonymous pulls are limited to **100 pulls per 6 hours per IP**. In a university or shared network environment where many students share a single outgoing IP address, this limit can be hit quickly — the pull will fail with a `429 Too Many Requests` error.

To work around this, log in to Docker Hub before pulling:

```bash
docker login
```

A free Docker Hub account raises the limit to **200 pulls per 6 hours** per account.


Your cluster might fail to start due to failing bootstrap checks. Find the following workarounds below.

### Sneaky way

Set `bootstrap.memory_lock` to `false` in your [docker-compose.yml](./docker-compose.yml) to skip the bootstrap checks. This is not suitable for production!

```yaml
- bootstrap.memory_lock=false
```

### Set required node settings

In production you would want to run the bootstrap checks to ensure your node is configured properly. Here you find the important settings that must be set:<br>
[https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html)
