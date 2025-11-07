# Kibana Users Ansible Role

This Ansible role creates multiple Kibana users with developer permissions for Elasticsearch and Kibana. The users can create indices, use the Dev Tools UI, access Elasticsearch cluster health metrics, and use Kibana's Enterprise Search Web Crawler.

## Features

- **Web Crawler Support**: Users have full access to Kibana's Enterprise Search and Web Crawler features
- **Smart Updates**: Only updates existing users if their roles have changed, avoiding unnecessary modifications
- **Idempotent**: Safe to run multiple times - skips users that already exist with correct roles
- **Comprehensive Permissions**: Full access to Discover, Visualize, Dashboard, Dev Tools, and Enterprise Search

## Requirements

- Ansible 2.9 or higher
- Access to an Elasticsearch cluster with admin credentials
- Elasticsearch Security features enabled
- Kibana connected to the Elasticsearch cluster

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

### Elasticsearch Connection

```yaml
elasticsearch_host: "localhost"
elasticsearch_port: 9200
elasticsearch_protocol: "https"
elasticsearch_admin_user: "admin"
elasticsearch_admin_password: ""
```

### User Configuration

```yaml
# Number of users to create (customizable)
kibana_users_count: 5

# Base username prefix (users will be named: kibana_user1, kibana_user2, etc.)
kibana_user_prefix: "kibana_user"

# Default password for created users (should be changed on first login)
kibana_user_default_password: "ChangeMe123!"

# Role name for the users
kibana_user_role_name: "kibana_developer"
```
