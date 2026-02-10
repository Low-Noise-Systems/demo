# Example Script Repo (Sea)

This folder is a sample Git repository layout for Sea "Script Repos" sync.

Rules:
- Sea scans **top-level directories**.
- A directory is treated as a script if it contains `manifest.yml`.
- `manifest.yml` must contain a stable `id` (UUID string). This allows renaming `name` without losing identity/history.
- `entry` must be a **relative path** inside the script folder.

Included examples:
- `hello-python/` (multi-file Python)
- `hello-powershell/` (PowerShell)
- `hello-ansible/` (Ansible)
