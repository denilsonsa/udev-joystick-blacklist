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

### Learning more about udev rules

* Nice (but outdated) udev tutorial: <http://www.reactivated.net/writing_udev_rules.html>.
* Debugging udev rules: <http://www.jpichon.net/blog/2011/12/debugging-udev-rules/>.
* Monitoring and debugging kernel and udev events: `udevadm monitor -p`
* Documentation: <http://www.freedesktop.org/software/systemd/man/udev.html> (and also the manpages installed on your system).

## Testing joystick detection

These tools list and interact with all available/detected joysticks:

* **jstest-gtk**
    * <https://github.com/Grumbel/jstest-gtk/>
    * [Directly interacts with `/dev/input/js*` devices. No library is used.](https://github.com/Grumbel/jstest-gtk/blob/2355f44f571a6d5f4ff4dfaf3a27ee223fb91ed7/src/joystick.cpp#L43)
    * [Detects up to 32 devices with `/dev/input/js*` path.](https://github.com/Grumbel/jstest-gtk/blob/2355f44f571a6d5f4ff4dfaf3a27ee223fb91ed7/src/joystick.cpp#L132)
* **pygame-joystick-test.py**
    * <https://bitbucket.org/denilsonsa/pygame-joystick-test/>
    * <https://bitbucket.org/denilsonsa/pygame-joystick-test/src/default/pygame-joystick-test.py>
    * Uses Python 2.x and [Pygame](http://www.pygame.org/), which uses SDL.

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
