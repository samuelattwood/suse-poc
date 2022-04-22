# SUSE Connect API POC
Example code for querying the SUSE SCC Connect API

Intended to be used with the repositories endpoint - [https://scc.suse.com/connect/organizations/repositories](https://scc.suse.com/connect/organizations/repositories)

Expected credentials are the "Mirroring credentials" as provided in [SUSE Customer Center](https://scc.suse.com/)

[API Documentation](https://scc.suse.com/connect/v4/documentation#)


```bash
$ pip install -r requirements.txt
$ python3 scc-query.py
Username: aabbccddee
Password:
URL: https://scc.suse.com/connect/organizations/repositories
Product: SLE-Module-Python3-15-SP4-Pool
Product Description: SLE-Module-Python3-15-SP4-Pool for sle-15-x86_64
Distro Target: sle-15-x86_64
Name: python310
License: Python-2.0
Arch: x86_64
Version: 3.10.2-150400.2.5
Checksum: 81d806dae8ec0cdd4752da64da20d0ebb670ab56821b4cc460b71dc2a2e2be25
URL: https://updates.suse.com/SUSE/Products/SLE-Module-Python3/15-SP4/x86_64/product/x86_64/python310-3.10.2-150400.2.5.x86_64.rpm
```
