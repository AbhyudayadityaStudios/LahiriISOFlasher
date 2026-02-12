Inside the subfolders, there are third-party files.

* The 'boot' folder contains bootcodes and 'UEFI-NTFS.img' used by Rufus.
  After bootable pendrive creation using Rufus, the binary files were extracted using
  this command in Cygwin with Administrative Privileges and then renamed:
      dd if=\\.\PHYSICALDRIVE1 of=/usr/bootcode.bin bs=512 count=1
  And 'UEFI-NTFS.img' from: 
      https://github.com/pbatard/rufus
      at '/res/uefi/uefi-ntfs.img'

* The 'additional' folder contains files which are placed by Rufus after creation of
  MS-DOS, FreeDOS, Syslinux 4.07, Syslinux 6.04 and Grub4DOS 0.4.6a. E.g. grldr, 
  COMMAND.COM, KERNEL.SYS, IO.SYS and etc.

* The 'cygwin' folder contains files from Cygwin to use 'dd' and 'mke2fs' commands on
  Windows. Here's a list of the files, the packages it belongs to and the official 
  projects:
    +--------------------+----------------------+---------------------+
    | File Name          | Package Name         | Project Name        |
    +--------------------+----------------------+---------------------+
    | cygblkid-1.dll     | libblkid1-2.40.2-2   | E2fsprogs           |
    | cygcom_err-2.dll   | libcom_err2-1.44.5-1 | E2fsprogs           |
    | cyge2p-2.dll       | libe2p2-1.44.5-1     | E2fsprogs           |
    | cygext2fs-2.dll    | libext2fs2-1.44.5-1  | E2fsprogs           |
    | cyggcc_s-seh-1.dll | libgcc1-13.4.0-1     | GCC Runtime Library |
    | cygiconv-2.dll     | libiconv2-1.17-1     | GNU gettext         |
    | cygintl-8.dll      | libintl8-0.22.5-1    | GNU gettext         |
    | cyguuid-1.dlll     | libuuid1-2.40.2-2    | E2fsprogs           |
    | cygwin1.dll        | cygwin-3.6.5-1       | Cygwin              |
    | dd.exe             | coreutils-9.0-1      | GNU Core Utilities  |
    | mke2fs.exe         | e2fsprogs-1.44.5-1   | E2fsprogs           |
    +--------------------+----------------------+---------------------+

* The 'jdk' folder contains files from Java Development Kit v24.0.1 to use the
  commands discussed above. The files inside 'jdk' and 'cygwin' are indicated
  by 'cygcheck' command in Cygwin.
