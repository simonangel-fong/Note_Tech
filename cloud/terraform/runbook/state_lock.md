# Runbook - State Lock

[Back](../index.md)

- [Runbook - State Lock](#runbook---state-lock)
  - [State Lock](#state-lock)
    - [Solution](#solution)
    - [!!Force unlock fails](#force-unlock-fails)

---

## State Lock

- Senario:
  - tf apply
  - network disconnect
  - reapply

```txt
terraform -chdir=infra/aws apply -auto-approve
╷
│ Error: Error acquiring the state lock
│
│ Error message: operation error S3: PutObject, https response error StatusCode: 412, RequestID: M0PDDF9NFJZTPV1J, HostID:
│ 2Rtlp2mhZ+fZEEPjPxG/zkxbwOPrs8Zh9L5oip3C6Vxea/pfjZTubva/Z/aOuh7XXoqZnfGHkvMqkxGmtFBlTe9dwt9jS6Mb, api error
│ PreconditionFailed: At least one of the pre-conditions you specified did not hold
│ Lock Info:
│   ID:        5da9daa4-d6a6-eacd-bc53-bab5eec3be6e
│   Path:      ******/terraform.tfstate
│   Operation: OperationTypeApply
│   Who:       **********
│   Version:   1.15.2
│   Created:   2026-06-24 17:28:33.4529028 +0000 UTC
│   Info:
│
│
│ Terraform acquires a state lock to protect the state from being written
│ by multiple users at the same time. Please resolve the issue above and try
│ again. For most commands, you can disable locking with the "-lock=false"
│ flag, but this is not recommended.
```

### Solution

1. Make sure no apply is actually still running

- Check Task Manager for any terraform.exe process. Kill it if you find one.
- If you ran apply in another terminal, close that terminal.

2. Force-unlock using the lock ID from the error

- The error gave you the lock ID: `<lock_ID>`

```sh
terraform -chdir=infra/aws force-unlock lock_ID

# Do you really want to force-unlock?
#   Terraform will remove the lock on the remote state.
#   This will allow local Terraform commands to modify this state, even though it
#   may still be in use. Only 'yes' will be accepted to confirm.

#   Enter a value: yes

# Terraform state has been successfully unlocked!

# The state has been unlocked, and Terraform commands should now be able to
# obtain a new lock on the remote state.
```

3. Refresh state, then re-apply

- Run a plan to preview what will get changed

```sh
terraform -chdir=infra/aws plan


terraform -chdir=infra/aws apply


```

---

### !!Force unlock fails

- If force-unlock itself fails, you can manually delete the lock object from S3:

```sh
aws s3api delete-object --bucket bucket_name --key <key_name>/terraform.tfstate.tfloc
```
