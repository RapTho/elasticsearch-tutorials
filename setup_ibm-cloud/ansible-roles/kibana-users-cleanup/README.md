# Kibana Users Cleanup Ansible Role

This Ansible role deletes Kibana users and roles that were created by the `kibana-users` role. It identifies users by their prefix and removes them along with the associated custom role.

## What This Role Does

1. **Discovers Users**: Queries Elasticsearch for all users matching the specified prefix
2. **Confirmation**: Prompts for confirmation before deletion (can be disabled)
3. **Deletes Users**: Removes all users with the matching prefix
4. **Deletes Role**: Removes the custom Kibana developer role
5. **Summary**: Displays a summary of deleted resources

## Requirements

- Ansible 2.9 or higher
- Access to an Elasticsearch cluster with admin credentials
- Elasticsearch Security features enabled

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

### Cleanup Configuration

```yaml
# Base username prefix (must match the prefix used during user creation)
kibana_user_prefix: "kibana_user"

# Role name (must match the role name used during creation)
kibana_user_role_name: "kibana_developer"

# Confirm deletion (set to false to skip confirmation prompt)
confirm_deletion: true
```
