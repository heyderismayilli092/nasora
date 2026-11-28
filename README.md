# nasora

A lightweight FastAPI-based NAS file management API with a Python SDK for remote file transfers and storage operations.

By configuring the `config.json` file on the server, you can specify which directory will be shared. Once the server is running, other computers on the same network can interact with that directory using the Nasora Python client.

Nasora provides a simple interface for file transfers, directory management, remote command execution, and file information retrieval.

## How It Works

Nasora consists of two main components:

- **Server:** Shares a directory on the host computer based on the settings defined in `config.json`.
- **Client:** Provides Python functions to interact with the shared directory remotely.

The client does not need to manage the server's internal implementation. It only needs the server's IP address and the appropriate function parameters.

## Getting Started

### 1. Configure the Server

Edit the `config.json` file to specify the directory you want to share.

The configured directory becomes the root directory for all remote operations.

### 2. Import the Client

On the client computer, import Nasora:

```python
from nasora.client import nasora
```

You can now access the remote directory using the available functions.

## API Reference

All functions are accessed through the `nasora` module.

| Function | Description |
|---|---|
| `nasora.send_file(filename, remotepath, ipaddr)` | Sends a local file to the remote directory. |
| `nasora.command(command, remotepath, ipaddr)` | Executes a command inside the specified remote directory. |
| `nasora.directory_list(remotepath, ipaddr)` | Lists files and directories inside the specified remote directory. |
| `nasora.create_folder(foldername, ipaddr)` | Creates a new directory inside the shared root directory. |
| `nasora.delete_folder(foldername, ipaddr)` | Deletes a directory from the shared root directory. |
| `nasora.download(remotepath, filename, save_dir, ipaddr)` | Downloads a remote file to a specified local directory. |
| `nasora.info_file(remotepath, filename, ipaddr)` | Retrieves information about a remote file. |
| `nasora.delete_file(remotepath, filename, ipaddr)` | Deletes a file from the specified remote directory. |
| `nasora.info_folder(remotepath, ipaddr)` | Retrieves information about a remote directory. |
| `nasora.server_info(ipaddr)` | Retrieves server information. |

## Remote Path Usage

For example:

```python
# Access the shared root directory
nasora.directory_list(".", "192.168.1.15")

# Access a subdirectory
nasora.directory_list("folder1/folder2", "192.168.1.15")
```

For `create_folder()` and `delete_folder()`, paths are specified relative to the shared root directory, so no additional `remotepath` parameter is required.

## Usage Examples

### List Remote Files

```python
from nasora.client import nasora

ipaddr = "192.168.1.15"

files = nasora.directory_list(".", ipaddr)
print(files)
```

### Create a Directory

```python
nasora.create_folder("folder1/folder2/folder3", ipaddr)
```

This creates the following directory structure inside the shared folder:

```text
folder1/
└── folder2/
    └── folder3/
```

### Send a File

```python
nasora.send_file(
    "example.txt",
    ".",
    ipaddr
)
```

### Download a File

```python
nasora.download(
    ".",
    "example.txt",
    "/home/user/Downloads",
    ipaddr
)
```

### Get File Information

```python
info = nasora.info_file(".", "example.txt", ipaddr)
print(info)
```

### Execute a Remote Command

```python
output = nasora.command(
    "ls -la",
    ".",
    ipaddr
)
print(output)
```

### Delete a File

```python
nasora.delete_file(".", "example.txt", ipaddr)
```

### Get Directory Information

```python
info = nasora.info_folder(".", ipaddr)
print(info)
```

## Notes

- The server and client must be able to communicate over the local network.
- All remote paths are interpreted relative to the configured shared directory.
- The `.` notation always refers to the root of the shared directory.
- The `command()` function executes commands remotely. Only use this functionality on trusted servers and networks.

---

**Nasora — Simple remote directory management through Python.**

