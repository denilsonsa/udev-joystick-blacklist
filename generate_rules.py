#!/usr/bin/env python3

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

    # Microsoft® 2.4GHz Transceiver v9.0
    # Microsoft® Nano Transceiver v2.1
    # Microsoft Sculpt Ergonomic Keyboard (5KV-00001)
    ('045e', '07a5'),

    # Microsoft® Nano Transceiver v1.0
    # Microsoft Wireless Keyboard 800
    ('045e', '07b2'),

    # Microsoft® Nano Transceiver v2.0
    ('045e', '0800'),

    # WACOM CTE-640-U V4.0-3
    # Wacom Co., Ltd Graphire 4 6x8
    ('056a', '0016'),

    # Wacom Bamboo Pen and Touch CTH-460
    ('056a', '00d1'),

    # A4 Tech Co., G7 750 mouse
    ('09da', '054f'),

    # A4 Tech Co., Ltd Bloody TL80 Terminator Laser Gaming Mouse
    ('09da', '31b5'),

    # A4 Tech Co., Ltd Bloody RT7 Terminator Wireless
    ('09da', '3997'),

    # Modecom MC-5006 Keyboard
    ('09da', '51f4'),

    # A4 Tech Co., Ltd Terminator TL9 Laser Gaming Mouse
    ('09da', '5589'),

    # A4 Tech Co., Ltd Bloody V5
    ('09da', '7b22'),

    # A4 Tech Co., Ltd Bloody R3 mouse
    ('09da', '7f2d'),

    # A4 Tech Co., Ltd X-718BK Oscar Optical Gaming Mouse
    ('09da', '8090'),

    # A4 Tech Co., Ltd XL-750BK Laser Mouse
    ('09da', '9090'),

    # A4 Tech Co., Sharkoon Fireglider Optical
    ('09da', '9066'),

    # Cooler Master Storm Mizar Mouse
    ('2516', '001f'),
]


def main():
    with open('51-these-are-not-joysticks.rules', 'w') as f:
        f.write(textwrap.dedent('''\
            # /etc/udev/rules.d/51-these-are-not-joysticks.rules
            #
            # This file is auto-generated. For more information:
            # https://github.com/denilsonsa/udev-joystick-blacklist

            '''))
        for vendor, product in DEVICES:
            f.write('SUBSYSTEM=="input", ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", ENV{ID_INPUT_JOYSTICK}=="?*", MODE="0000", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))
            f.write('SUBSYSTEM=="input", ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", KERNEL=="js[0-9]*", MODE="0000", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))

    with open('51-these-are-not-joysticks-rm.rules', 'w') as f:
        f.write(textwrap.dedent('''\
            # /etc/udev/rules.d/51-these-are-not-joysticks-rm.rules
            #
            # This file is auto-generated. For more information:
            # https://github.com/denilsonsa/udev-joystick-blacklist

            '''))
        for vendor, product in DEVICES:
            f.write('SUBSYSTEM=="input", ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", ENV{ID_INPUT_JOYSTICK}=="?*", RUN+="/bin/rm %%E{DEVNAME}", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))
            f.write('SUBSYSTEM=="input", ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", KERNEL=="js[0-9]*", RUN+="/bin/rm %%E{DEVNAME}", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))


if __name__ == '__main__':
    main()
