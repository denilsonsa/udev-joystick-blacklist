# udev-joystick-blacklist

Fix for keyboard/mouse/tablet being detected as joystick in Linux.

There are several devices that, although recognized by kernel as joysticks, are not joysticks. This repository contains rules that will prevent the non-functional `/dev/input/js*` and `/dev/input/event*` devices from being recognized as joysticks.

This is just a blacklist, which will always be incomplete (until the actual bug gets fixed). Feel free to add more devices to this list.

## Known devices

For the complete list, look at the [`generate_rules.py`](generate_rules.py) script.

* A4 Tech mice and/or keyboards.
* ASRock LED controller.
* Cooler Master mice.
* Corsair mice and/or keyboards.
* Lenovo keyboard.
* Microsoft mice and/or keyboards. ([Fixed in Linux kernel 4.9.](https://github.com/denilsonsa/udev-joystick-blacklist/issues/20))
* Wacom tablets.
* …and many others!

## How to install

### Version that changes permissions to 0000

    sudo curl -o /etc/udev/rules.d/51-these-are-not-joysticks.rules \
      https://raw.githubusercontent.com/denilsonsa/udev-joystick-blacklist/master/51-these-are-not-joysticks.rules

### Version that removes the device

    sudo curl -o /etc/udev/rules.d/51-these-are-not-joysticks-rm.rules \
      https://raw.githubusercontent.com/denilsonsa/udev-joystick-blacklist/master/51-these-are-not-joysticks-rm.rules

### Which version should I use?

Personally, I'd try the first version (that sets permissions to `0000`) first. If it does not work or if it gives trouble for some reason, I'd try the second version (that removes the device).

The first version (that sets permissions to `0000`) seems to work fine across several distros, but some distros ([such as OSMC](https://github.com/denilsonsa/udev-joystick-blacklist/issues/5#issuecomment-151872841), [see also issue #26](https://github.com/denilsonsa/udev-joystick-blacklist/issues/26)) may have additional rules that end up setting the permssions back to another value. In such case, the second version (that removes the device) should work.

In the end, it's up to you, and it's about what works best for you and your system.

### What's different in `after_kernel_4_9/`?

A patch has been accepted into Linux kernel 4.9, so that Microsoft devices will not be detected as joysticks anymore. Thus, those devices are not included in `after_kernel_4_9/*`. Read [issue #20](https://github.com/denilsonsa/udev-joystick-blacklist/issues/20) for details.

## How it works

### Matching

A rule will match if:

* The subsystem is `input`;
* The pair `idVendor` and `idProduct` is in this list;
* Either one of:
    * The device property `ID_INPUT_JOYSTICK` is set;
    * Or the device name matches `js[0-9]*`.

### Actions

The following actions are taken on each matching rule:

* Clears `ID_INPUT_JOYSTICK` property, which prevents [some `/lib/udev/rules.d/*` rules from running](https://github.com/denilsonsa/udev-joystick-blacklist/issues/5#issuecomment-151832071).
* Depending on which version you installed, one of the following extra actions are applied only for `/dev/input/js*`:
    * [Removes read and write permissions by setting `MODE="0000"`](https://en.wikipedia.org/wiki/File_system_permissions#Numeric_notation). This effectively prevents the device from being used.
    * Removes the device file from `/dev/input/`. This also prevents the device from being found or from being listed.

It is not possible to rename a device, so `NAME="not-a-joystick%n"` will not work.

### Learning more about udev rules

* Documentation: <http://www.freedesktop.org/software/systemd/man/udev.html> (and also the manpages installed on your system).
* Debugging udev rules: <http://www.jpichon.net/blog/2011/12/debugging-udev-rules/>.
* Nice (but outdated) udev tutorial: <http://www.reactivated.net/writing_udev_rules.html>.

## Troubleshooting

Look at the generated `/dev` files: `ls -l /dev/input/`

Unplug and plug your USB device while monitoring for kernel and udev events: `udevadm monitor -p`

Look for other udev rules that may interact with the same device: `grep -i '\bjs\b\|joystick' /lib/udev/rules.d/* /usr/lib/udev/rules.d/* /etc/udev/rules.d/*`

## Testing joystick detection

These tools list and interact with all available/detected joysticks:

* **jstest-gtk**
    * <https://github.com/Grumbel/jstest-gtk/>
    * [Directly interacts with `/dev/input/js*` devices. No library is used.](https://github.com/Grumbel/jstest-gtk/blob/17956d285fedcf476ea753ff850fa7adf51ba07c/src/joystick.cppL42)
    * [Detects up to 32 devices with `/dev/input/js*` path.](https://github.com/Grumbel/jstest-gtk/blob/17956d285fedcf476ea753ff850fa7adf51ba07c/src/joystick.cpp#L152-L161)
* **pygame-joystick-test.py**
    * <https://github.com/denilsonsa/pygame-joystick-test/>
    * Uses Python (2.x or 3.x) and [Pygame](http://www.pygame.org/), which uses [SDL](https://www.libsdl.org/).
* **sdl-jstest --list** and **sdl2-jstest --list**
    * <https://gitlab.com/sdl-jstest/sdl-jstest>
    * Uses [SDL](https://www.libsdl.org/) and prints the detected joysticks to stdout.
    * SDL1 looks at [the first 32 devices](https://github.com/libsdl-org/SDL-1.2/blob/52c714024e2d5a5383f64f9b119ea96cb46f9af2/src/joystick/linux/SDL_sysjoystick.c#L258-L259) named [`/dev/input/js*` or `/dev/js*`](https://github.com/libsdl-org/SDL-1.2/blob/52c714024e2d5a5383f64f9b119ea96cb46f9af2/src/joystick/linux/SDL_sysjoystick.c#L405-L411).
        * [As a special case, it can also look at `/dev/input/event*`](https://github.com/libsdl-org/SDL-1.2/blob/52c714024e2d5a5383f64f9b119ea96cb46f9af2/src/joystick/linux/SDL_sysjoystick.c#L496-L506).
    * SDL2 can either use [`libudev` or `inotify` or just plain polling](https://github.com/libsdl-org/SDL/blob/1bf7898ddf1e0d6a6dd391614fd86f3731349fe2/src/joystick/linux/SDL_sysjoystick.c#L878-L892) to read entries from `/dev/input/`.
* **wine control.exe joy.cpl**
    * <https://www.winehq.org/>
    * The [Wine control panel](http://wiki.winehq.org/control) includes a *Game Controllers* configuration.
    * It can look at [the first 64 devices](https://source.winehq.org/git/wine.git/blob/dca0e38d82c737cd8aeab63e08cf1990d05d9671:/dlls/dinput/joystick_linux.c#l139) named [`/dev/input/js*` or `/dev/js*`](https://source.winehq.org/git/wine.git/blob/dca0e38d82c737cd8aeab63e08cf1990d05d9671:/dlls/dinput/joystick_linux.c#l72).
    * It can look at [the first 64 devices](https://source.winehq.org/git/wine.git/blob/dca0e38d82c737cd8aeab63e08cf1990d05d9671:/dlls/dinput/joystick_linuxinput.c#l180) named [`/dev/input/event*`](https://source.winehq.org/git/wine.git/blob/dca0e38d82c737cd8aeab63e08cf1990d05d9671:/dlls/dinput/joystick_linuxinput.c#l70).
* **steam -bigpicture**
    * <http://store.steampowered.com/bigpicture>
    * Valve's Steam → Big Picture mode → ⚙ Settings → Controller.
    * Uses SDL2 to detect joysticks.

## Contributing

The best ways to contribute are by [creating a new issue][issues] or by [making a pull request][forking]. Make sure you mention the device name/description and the vendor/product IDs. The relevant line from `lsusb` output is usually enough.

This repository contains a list of devices compiled from contributions of several people. I cannot test every single device. If something does not work for you even after you have added the correct rules, please try debugging it on your own system. The output of `udevadm monitor -p` may prove very helpful. Also look at the output of `ls -l /dev/input/`.

## Bug reports and mentions

There are reports of this issue on different distros and projects.

* <https://bugzilla.kernel.org/show_bug.cgi?id=28912>
* <https://bugzilla.kernel.org/show_bug.cgi?id=37982>
* <https://bugs.launchpad.net/ubuntu/+source/linux/+bug/390959>
* <https://askubuntu.com/questions/173376/how-do-i-disable-joystick-input>
* <https://ryort.wordpress.com/2011/12/04/udev-and-the-microsoft-digital-media-keyboard-3000-wha/>
* <https://bbs.archlinux.org/viewtopic.php?id=190485>
* <https://bbs.archlinux.org/viewtopic.php?id=142469>
* <https://forums.gentoo.org/viewtopic-t-362032.html>
* <https://bugs.winehq.org/show_bug.cgi?id=35954>
* <https://github.com/ValveSoftware/steam-for-linux/issues/3943>

The udev rules in this repository have been added to:

* Debian and Ubuntu
    * [Debian bug #714399](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=714399)
    * `joystick` package, starting on version 1.4.9-1
* Arch Linux and derivatives (such as Manjaro)
    * [AUR package udev-joystick-blacklist](https://aur.archlinux.org/packages/udev-joystick-blacklist)
* SDL library
    * [SDL_ShouldIgnoreJoystick() inside SDL_joystick.c](https://github.com/spurious/SDL-mirror/blob/master/src/joystick/SDL_joystick.c#L2188C10-L2317)
    * [Originally added only for Linux on 2017-04-06](https://github.com/spurious/SDL-mirror/commit/3b03af8b7e2c7105ffce8843fe395e6f3b2e678b)
    * [Later expanded to other systems (such as Windows) on 2018-12-05](https://github.com/spurious/SDL-mirror/commit/87928f6cbd875c771b9647ff471ec6a37bd52491)

But remember that the version distributed elsewhere might be different than the version on this repository.

## Semi-related projects

* [game-devices-udev](https://codeberg.org/fabiscafe/game-devices-udev) - Collection of udev rules for game controllers, usually giving permission for the user to access those devices.

## History of this repository

After suffering with this issue for a long time, I decided to investigate possible fixes and workarounds. Then, in May 2015, after searching a lot for a solution, I've managed to create some udev rules that fixed the issue for my devices and decided to share this solution with other people. Initially, I shared [the simple file at GitHub Gist][gist]. Over time, people submitted contributions through comments, and keeping that file on Gist was becoming too hard to manage.

In October 2015, I decided to move the file to [this GitHub repository][github]. That way, it will be easier to make changes, to fork, to receive notifications, and essentially to maintain it.

Ideally, the bug in the Linux kernel should be fixed, so that this repository (which is essentially just a workaround) wouldn't be needed anymore. However, it's also possible those devices are incorrectly reporting their own capabilities, and thus the operating system is just following the device descriptors. Given there is [a report of this issue on Windows](https://github.com/spurious/SDL-mirror/commit/87928f6cbd875c771b9647ff471ec6a37bd52491), that could be the case.

## License

Public domain. Feel free to use this project for whatever purpose you want.

Also, feel free to contribute to the project. And, if you have the knowledge and the skills, consider fixing this bug in the Linux kernel itself.

There is no warranty implied by using this project. Use at your own risk.


[gist]: https://gist.github.com/denilsonsa/978f1d842cf5430f57f6
[github]: https://github.com/denilsonsa/udev-joystick-blacklist
[issues]: https://github.com/denilsonsa/udev-joystick-blacklist/issues
[forking]: https://guides.github.com/activities/forking/
