================================================================================
Data Integrity
================================================================================

https://en.wikipedia.org/wiki/Error_detection_and_correction

--------------------------------------------------------------------------------
CRC / LRC
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
Hamming Code
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
MD5
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
Merkle Tree
--------------------------------------------------------------------------------

https://en.wikipedia.org/wiki/Merkle_tree
http://docs.aws.amazon.com/amazonglacier/latest/dev/checksum-calculations.html

--------------------------------------------------------------------------------
Reed Solomon Encoding
--------------------------------------------------------------------------------

https://github.com/Backblaze/JavaReedSolomon

--------------------------------------------------------------------------------
RAID
--------------------------------------------------------------------------------

* **RAID 0**

  This works by simply striping writes across one or more disks. It adds no
  checksum information (thus any errors may ruin a file in question), however by
  writing a slice of each file on a different disk it increases write / read
  throughput.

  This can also be used to create one large disk out of several smaller disks.
  It should be noted that if striping is used, increases in size can only be
  added as a factory of the smallest disk (unless a more complex scheme is used).

* **RAID 1**

  This works by creating a mirror of all the data across all the disks. This
  essentially creates N backups of the given data. As there are many copies of
  the same data, read performance can be increased by a factor of N by performing
  parallel reads of different blocks across the array. It should be noted that
  write performance is limited by the write speed of the slowest disk (unless a
  more complex scheme is used).

* **RAID 2**

  This works by striping the data at the bit level across all the disks and then
  using a hamming error code. In order for this to work at high speeds, all the
  drives have to be calibrated to spin at the same index. This RAID technique is
  no longer used as the controller is usually too expensive and modern drives
  perform internal error correction which reduces the need for the hamming code.

* **RAID 3**

  This is like RAID 2 with striping at the byte level and a dedicated parity disk.
  It is no longer in use, but was used for high transfer rates of large amounts of
  data (like uncompressed video streams). It should be noted that simultaneous
  requests could not be served as all disks must be synced.

* **RAID 4**

  This is RAID 3 at the block level.

* **RAID 5**

  This is the replacement for RAID 3 and 4. It works by striping at the block level
  and distributing the parity information across the drives. This gave the advantage
  that parity and read operations were smoothed across all the drives.

  Continuing, although this needs at least three drives to operate, if one of the drives
  fails, the original data can still be recreated with the remaining parity information.

* **RAID 6**

  This is RAID 5 with another parity disk. Essentially this can be seen as Reed Solomon
  coding. The read performance is not penalized, however the write performance is (as 
  a result of the extra parity information written). As such, modern implementations
  are implemented in hardware / firmware.
