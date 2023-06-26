# Audubon Racing Motor Driver Stack

This ROS package contains a collections of packages that interface with the racer and the hardware.


## Stack Pipeline
### Input Specifications

### Output Specifications

## VESC Setup

As the vesc connects over serial port, we need to create a serial passthrough port for the vesc.

### Steps

1. Find the VESC attributes

Use following commands to find the `\<idVendor\>` and `\<idProduct\>`

```console
lsusb
udevadm info
udevadm info -a -n /dev/sdb | less
udevadm info -a -n /dev/sdb | grep vendor
```

2. Setup `udev` rule for `symlink`

Add the rule to `80-local.rules` in `/etc/udev/rules.d`

```console
SUBSYSTEM=="tty", ATTRS{idVendor}=="<idVendor>", ATTRS{idProduct}=="<idProduct>", MODE="0777", SYMLINK+="ttyVESC"
```

Most likely the details will be this:-
    idProduct = 5740
    idVendor = 0483

Then run udevadm control --reload to try but reboot after completing all steps is the best way to test the rules.

3. Setup `chmod` in `bash_aliases`
Only need to add the connection permissions to the symlink.

```console
chmod 777 /dev/ttyVESC
```

4. Reboot the device.

As the udev admin has to be reset for the rule to be activated, we can only truly test the setup on reboot.

5. Verify the simlink and permissions for VESC.