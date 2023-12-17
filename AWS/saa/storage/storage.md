# AWS Storage - Summary

[Back](../index.md)

- [AWS Storage - Summary](#aws-storage---summary)
  - [Summary: Storage Comparison](#summary-storage-comparison)

---

## Summary: Storage Comparison

- `S3`:
  - **Object** Storage
- `S3 Glacier`:
  - Object **Archival**
- `EBS volumes`:
  - **Network storage** for one **EC2 instance** at a time
- `Instance Storage`:
  - **Physical** storage for your EC2 instance (**high IOPS**)
- `EFS`:
  - **Network File System** for **Linux** instances, `POSIX(Portable Operating System Interface)` filesystem
- `FSx for Windows`:
  - **Network File System** for **Windows servers**
- `FSx for Lustre`:
  - **High Performance Computing** **Linux** file system
- `FSx for NetApp ONTAP`:
  - High **OS Compatibility**
- `FSx for OpenZFS`:
  - Managed **ZFS file system**
- `Storage Gateway`: bridge storage between on-premises and AWS
  - `S3 & FSx File Gateway`
  - `Volume Gateway (cache & stored)`
  - `Tape Gateway`
- `Transfer Family`:
  - **FTP, FTPS, SFTP interface** on top of Amazon S3 or Amazon EFS
- `DataSync`:
  - **Schedule data sync** from on-premises to AWS, or AWS to AWS
- `Snowcone / Snowball / Snowmobile`:
  - to move large amount of data to the cloud, **physically**
- `Database`:
  - for specific workloads, usually with **indexing** and **querying**

---

- Types of Various Units of Memory
  - Bit
  - Nibble
  - Byte
  - Kilo Byte
  - MegaByte
  - Giga Byte
  - Tera Byte
  - Peta Byte
  - Exa Byte
  - Zetta Byte
  - Yotta Byte

---

[TOP](#aws-storage---summary)
