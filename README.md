# MyControl Example Script Repository

This is an example repository for use with MyControl's script repository import feature.

## Structure

Each top-level directory contains a script with its `manifest.yml` descriptor:

```
install-nginx/       - Ansible playbook to install and configure Nginx
check-disk-space/    - Python script to check disk usage and alert
update-packages/     - Ansible playbook to update system packages
collect-system-info/ - Python script to gather system information
```

## manifest.yml format

| Field         | Type     | Required | Description                              |
|---------------|----------|----------|------------------------------------------|
| `name`        | string   | yes      | Display name of the script               |
| `description` | string   | no       | Brief description                        |
| `type`        | string   | yes      | `ansible`, `python`, or `powershell`     |
| `category`    | string   | no       | Folder/category name (auto-created)      |
| `os`          | string[] | no       | Target operating systems                 |
| `entry`       | string   | yes      | Main script filename                     |
| `timeout`     | integer  | no       | Execution timeout in seconds (default: 3600) |
| `verbosity`   | integer  | no       | Ansible verbosity 0-4 (default: 0)       |
| `tags`        | string[] | no       | Tags for filtering                       |
