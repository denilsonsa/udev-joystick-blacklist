#!/usr/bin/env python3

import os.path
import textwrap

# List of tuples ('idVendor', 'idProduct'), as four hexadecimal digits.
DEVICES = [
    # Microsoft Microsoft Wireless Optical Desktop® 2.10
    # Microsoft Wireless Desktop - Comfort Edition
    ('045e', '009d'),

    # Microsoft Microsoft® Digital Media Pro Keyboard
    # Microsoft Corp. Digital Media Pro Keyboard
    ('045e', '00b0'),

    # Microsoft Microsoft® Digital Media Keyboard
    # Microsoft Corp. Digital Media Keyboard 1.0A
    ('045e', '00b4'),

    # Microsoft Microsoft® Digital Media Keyboard 3000
    ('045e', '0730'),

    # Microsoft Microsoft® 2.4GHz Transceiver v6.0
    # Microsoft Microsoft® 2.4GHz Transceiver v8.0
    # Microsoft Corp. Nano Transceiver v1.0 for Bluetooth
    # Microsoft Wireless Mobile Mouse 1000
    # Microsoft Wireless Desktop 3000
    ('045e', '0745'),

    # Microsoft® SideWinder(TM) 2.4GHz Transceiver
    ('045e', '0748'),

    # Microsoft Corp. Wired Keyboard 600
    ('045e', '0750'),

    # Microsoft Corp. Sidewinder X4 keyboard
    ('045e', '0768'),

    # Microsoft Corp. Arc Touch Mouse Transceiver
    ('045e', '0773'),

    # Microsoft® 2.4GHz Transceiver v9.0
    # Microsoft® Nano Transceiver v2.1
    # Microsoft Sculpt Ergonomic Keyboard (5KV-00001)
    ('045e', '07a5'),

    # Microsoft® Nano Transceiver v1.0
    # Microsoft Wireless Keyboard 800
    ('045e', '07b2'),

    # Microsoft® Nano Transceiver v2.0
    ('045e', '0800'),

    # List of Wacom devices at: http://linuxwacom.sourceforge.net/wiki/index.php/Device_IDs
    ('056a', '0010'),  # Wacom ET-0405 Graphire
    ('056a', '0011'),  # Wacom ET-0405A Graphire2 (4x5)
    ('056a', '0012'),  # Wacom ET-0507A Graphire2 (5x7)
    ('056a', '0013'),  # Wacom CTE-430 Graphire3 (4x5)
    ('056a', '0014'),  # Wacom CTE-630 Graphire3 (6x8)
    ('056a', '0015'),  # Wacom CTE-440 Graphire4 (4x5)
    ('056a', '0016'),  # Wacom CTE-640 Graphire4 (6x8)
    ('056a', '0017'),  # Wacom CTE-450 Bamboo Fun (4x5)
    ('056a', '0016'),  # Wacom CTE-640 Graphire 4 6x8
    ('056a', '0017'),  # Wacom CTE-450 Bamboo Fun 4x5
    ('056a', '0018'),  # Wacom CTE-650 Bamboo Fun 6x8
    ('056a', '0019'),  # Wacom CTE-631 Bamboo One
    ('056a', '00d1'),  # Wacom Bamboo Pen and Touch CTH-460

    ('09da', '054f'),  # A4 Tech Co., G7 750 mouse
    ('09da', '3043'),  # A4 Tech Co., Ltd Bloody R8A Gaming Mouse
    ('09da', '31b5'),  # A4 Tech Co., Ltd Bloody TL80 Terminator Laser Gaming Mouse
    ('09da', '3997'),  # A4 Tech Co., Ltd Bloody RT7 Terminator Wireless
    ('09da', '3f8b'),  # A4 Tech Co., Ltd Bloody V8 mouse
    ('09da', '51f4'),  # Modecom MC-5006 Keyboard
    ('09da', '5589'),  # A4 Tech Co., Ltd Terminator TL9 Laser Gaming Mouse
    ('09da', '7b22'),  # A4 Tech Co., Ltd Bloody V5
    ('09da', '7f2d'),  # A4 Tech Co., Ltd Bloody R3 mouse
    ('09da', '8090'),  # A4 Tech Co., Ltd X-718BK Oscar Optical Gaming Mouse
    ('09da', '9066'),  # A4 Tech Co., Sharkoon Fireglider Optical
    ('09da', '9090'),  # A4 Tech Co., Ltd XL-730K / XL-750BK / XL-755BK Laser Mouse
    ('09da', '90c0'),  # A4 Tech Co., Ltd X7 G800V keyboard
    ('09da', 'f012'),  # A4 Tech Co., Ltd Bloody V7 mouse
    ('09da', 'f32a'),  # A4 Tech Co., Ltd Bloody B540 keyboard
    ('09da', 'f613'),  # A4 Tech Co., Ltd Bloody V2 mouse
    ('09da', 'f624'),  # A4 Tech Co., Ltd Bloody B120 Keyboard

    ('1d57', 'ad03'),  # [T3] 2.4GHz and IR Air Mouse Remote Control

    ('1e7d', '2e4a'),  # Roccat Tyon Mouse

    ('20a0', '422d'),  # Winkeyless.kr Keyboards

    ('2516', '001f'),  # Cooler Master Storm Mizar Mouse
    ('2516', '0028'),  # Cooler Master Storm Alcor Mouse
]


def write_mode_0000_udev_rule_file(path, devices, message):
    filename = os.path.basename(path)
    with open(path, 'w') as f:
        f.write('# /etc/udev/rules.d/' + filename + '\n' + message + '\n')
        f.write('ACTION!="add|change", GOTO="joystick_blacklist_end"\n')
        f.write('SUBSYSTEM!="input", GOTO="joystick_blacklist_end"\n')
        f.write('ENV{ID_INPUT_JOYSTICK}=="", GOTO="joystick_blacklist_end"\n\n')
        for vendor, product in devices:
            f.write('ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))
            f.write('ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", KERNEL=="js[0-9]*", MODE="0000"\n' % (vendor, product))
        f.write('\nLABEL="joystick_blacklist_end"\n')

def write_rm_udev_rule_file(path, devices, message):
    filename = os.path.basename(path)
    with open(path, 'w') as f:
        f.write('# /etc/udev/rules.d/' + filename + '\n' + message + '\n')
        f.write('ACTION!="add|change", GOTO="joystick_blacklist_end"\n')
        f.write('SUBSYSTEM!="input", GOTO="joystick_blacklist_end"\n')
        f.write('ENV{ID_INPUT_JOYSTICK}=="", GOTO="joystick_blacklist_end"\n\n')
        for vendor, product in devices:
            f.write('ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))
            f.write('ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", KERNEL=="js[0-9]*", RUN+="/bin/rm %%E{DEVNAME}"\n' % (vendor, product))
        f.write('\nLABEL="joystick_blacklist_end"\n')

def main():
    common_header = textwrap.dedent('''\
        #
        # This file is auto-generated. For more information:
        # https://github.com/denilsonsa/udev-joystick-blacklist
        ''')

    write_mode_0000_udev_rule_file('51-these-are-not-joysticks.rules', DEVICES, common_header)
    write_rm_udev_rule_file('51-these-are-not-joysticks-rm.rules', DEVICES, common_header)

    # See: https://github.com/denilsonsa/udev-joystick-blacklist/issues/20
    devices_except_microsoft = [dev for dev in DEVICES if dev[0] != '045e']
    write_mode_0000_udev_rule_file('after_kernel_4_9/51-these-are-not-joysticks.rules', devices_except_microsoft, common_header)
    write_rm_udev_rule_file('after_kernel_4_9/51-these-are-not-joysticks-rm.rules', devices_except_microsoft, common_header)


if __name__ == '__main__':
    main()
