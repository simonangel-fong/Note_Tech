# RHCSA Tune

[Back](../../index.md)

- [RHCSA Tune](#rhcsa-tune)
  - [Question](#question)
    - [Solution](#solution)

---

## Question

```conf
Configure recommended tuned profile
```

- In the exam, it mgith ask to change to a specific profile.

---

### Solution

```sh
# Install tuned
dnf install tuned -y
# Start and Enable the tuned Service
systemctl start tuned
systemctl enable tuned
# confirm
systemctl status tuned


# List Available Profiles
tuned-adm list
# Available profiles:
# - accelerator-performance     - Throughput performance based tuning with disabled higher latency STOP states
# - aws                         - Optimize for aws ec2 instances
# - balanced                    - General non-specialized tuned profile
# - balanced-battery            - Balanced profile biased towards power savings changes for battery
# - desktop                     - Optimize for the desktop use-case
# - hpc-compute                 - Optimize for HPC compute workloads
# - intel-sst                   - Configure for Intel Speed Select Base Frequency
# - latency-performance         - Optimize for deterministic performance at the cost of increased power consumption
# - network-latency             - Optimize for deterministic performance at the cost of increased power consumption, focused on low latency network performance
# - network-throughput          - Optimize for streaming network throughput, generally only necessary on older CPUs or 40G+ networks
# - optimize-serial-console     - Optimize for serial console use.
# - powersave                   - Optimize for low power consumption
# - throughput-performance      - Broadly applicable tuning that provides excellent performance across a variety of common server workloads
# - virtual-guest               - Optimize for running inside a virtual guest
# - virtual-host                - Optimize for running KVM guests
# Current active profile: virtual-guest

# Apply the Recommend Profile
tuned-adm recommend
# virtual-guest

# change to a specifi profile
tuned-adm profile balanced
# confirm
tuned-adm active
# Current active profile: balanced

# change back to recommend
tuned-adm recommend
# virtual-guest
tuned-adm profile virtual-guest
# confirm
tuned-adm active
# Current active profile: virtual-guest
```
