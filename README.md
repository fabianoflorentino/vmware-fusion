# **VMware Fusion API**

## **Documentation**

- [https://developer.vmware.com/apis/1044](https://developer.vmware.com/apis/1044)

```shell
Pre-requisites:
    export VMREST_URL=http://localhost:8697/api/vms
    export VMREST_AUTH=<AUTH_TOKEN>

    Ex. echo -n "username:password" | base64
        export VMREST_AUTH=Basic dXNlcm5hbWU6cGFzc3dvcmQ=

Usage: python3 api.py [OPTIONS]

Options:
    --api [enable|disable]             Enable or disable the VMware Fusion API
    --get-vm-list                      Get the list of VMs
    --get-vm-info [vm_id]              Get the info of a VM
    --get-vm-power-state [vm_id]       Get the power state of a VM
    --power-status [vm_id] [status]    VM power operations
                                        status: on, off, shutdown, suspend, pause, unpause
    --help, -h                         Show this help message and exit
```
