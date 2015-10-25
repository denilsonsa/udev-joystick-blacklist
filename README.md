# udev-joystick-blacklist

Fix for keyboard/mouse/tablet being detected as joystick in Linux.

There are several devices that, although recognized by kernel as joysticks, are not joysticks. This repository contains rules that will prevent the non-functional /dev/input/js* and /dev/input/event* devices from being used, by removing read/write permissions from them.

This is just a blacklist, which will always be incomplete (until the actual bug gets fixed). Feel free to add more devices to this list.

## How to install

    sudo curl -o /etc/udev/rules.d/51-these-are-not-joysticks.rules https://raw.githubusercontent.com/denilsonsa/udev-joystick-blacklist/master/51-these-are-not-joysticks.rules

## How it works

`MODE="0000"` removes read and write permissions, which prevents the device from being used.

Clearing `ID_INPUT_JOYSTICK` prevents some `/lib/udev/rules.d/*` rules from running.

It is not possible to rename a device, so `NAME="not-a-joystick%n"` does not work.

There is a nice (but outdated) udev tutoral at <http://www.reactivated.net/writing_udev_rules.html>.

## Bug reports and mentions

There are reports of this issue on different distros.

* <https://bugzilla.kernel.org/show_bug.cgi?id=28912>
* <https://bugzilla.kernel.org/show_bug.cgi?id=37982>
* <https://bugs.launchpad.net/ubuntu/+source/linux/+bug/390959>
* <https://askubuntu.com/questions/173376/how-do-i-disable-joystick-input>
* <https://ryort.wordpress.com/2011/12/04/udev-and-the-microsoft-digital-media-keyboard-3000-wha/>
* <https://forum.manjaro.org/index.php?topic=15275.msg144519#msg144519>
* <https://bbs.archlinux.org/viewtopic.php?id=190485>
* <https://bbs.archlinux.org/viewtopic.php?id=142469>
* <https://forums.gentoo.org/viewtopic-t-362032.html>
* <https://bugs.winehq.org/show_bug.cgi?id=35954>
* <https://github.com/ValveSoftware/steam-for-linux/issues/3943>

## Known devices

For the complete list, look at the actual udev rules.

* A4 Tech mouse and/or keyboard.
* Microsoft mouse and/or keyboard.
* Wacom tablets.

## History of this repository

After suffering with this issue for a long time, I decided to investigate possible fixes and workarounds. Then, in May 2015, after searching a lot for a solution, I've managed to create some udev rules that fixed the issue for my device, and decided to share this solution to other people. Initially, I shared [the simple file at GitHub Gist][gist]. Over time, people submitted contributions through comments, and keeping that file on Gist was becoming too hard to manage.

In October 2015, I decided to move the file to [this GitHub repository][github]. That way, it will be easier to make changes, to fork, to receive notifications, and essentially to maintain it.

Ideally, the bug in the Linux kernel would be fixed, so that this repository (which is essentially just a workaround) wouldn't be needed anymore.

[gist]: https://gist.github.com/denilsonsa/978f1d842cf5430f57f6
[github]: https://github.com/denilsonsa/udev-joystick-blacklist
