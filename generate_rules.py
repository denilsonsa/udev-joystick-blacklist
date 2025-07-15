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

    ('046b', 'ff10'),  # American Megatrends Inc. Virtual Keyboard and Mouse

    ('046d', 'c30a'),  # Logitech, Inc. iTouch Composite keboard

    ('04d9', '8009'),  # OBINS ANNE PRO 2 keyboard (Holtek Semiconductor USB-HID Keyboard)
    ('04d9', 'a0df'),  # Tek Syndicate Mouse (E-Signal USB Gaming Mouse)

    # List of Wacom devices at: https://github.com/linuxwacom/input-wacom/wiki/Device-IDs
    # It might be easier to create a custom rule to block all Wacom devices, based only on the Vendor ID.
    ('0531', '0100'),  # Wacom CTC4110WL Wacom One Pen tablet small
    ('0531', '0102'),  # Wacom CTC6110WL Wacom One Pen tablet medium
    ('0531', '0104'),  # Wacom CTC4110WL Wacom One Pen tablet small
    ('0531', '0105'),  # Wacom CTC6110WL Wacom One Pen tablet medium
    ('056a', '0003'),  # Wacom PTU-600 Cintiq Partner
    ('056a', '0010'),  # Wacom ET-0405 Graphire
    ('056a', '0011'),  # Wacom ET-0405A Graphire2 (4x5)
    ('056a', '0012'),  # Wacom ET-0507A Graphire2 (5x7)
    ('056a', '0013'),  # Wacom CTE-430 Graphire3 (4x5)
    ('056a', '0014'),  # Wacom CTE-630 Graphire3 (6x8)
    ('056a', '0015'),  # Wacom CTE-440 Graphire4 (4x5)
    ('056a', '0016'),  # Wacom CTE-640 Graphire4 (6x8)
    ('056a', '0017'),  # Wacom CTE-450 Bamboo Fun (4x5)
    ('056a', '0018'),  # Wacom CTE-650 Bamboo Fun (6x8)
    ('056a', '0019'),  # Wacom CTE-631 Bamboo One
    ('056a', '0020'),  # Wacom GD-0405 Intuos (4x5)
    ('056a', '0021'),  # Wacom GD-0608 Intuos (6x8)
    ('056a', '0022'),  # Wacom GD-0912 Intuos (9x12)
    ('056a', '0023'),  # Wacom GD-1212 Intuos (12x12)
    ('056a', '0024'),  # Wacom GD-1218 Intuos (12x18)
    ('056a', '0026'),  # Wacom PTH-450 Intuos5 touch (S)
    ('056a', '0027'),  # Wacom PTH-650 Intuos5 touch (M)
    ('056a', '0028'),  # Wacom PTH-850 Intuos5 touch (L)
    ('056a', '0029'),  # Wacom PTK-450 Intuos5 (S)
    ('056a', '002a'),  # Wacom PTK-650 Intuos5 (M)
    ('056a', '0030'),  # Wacom PL400
    ('056a', '0031'),  # Wacom PL500
    ('056a', '0032'),  # Wacom PL600
    ('056a', '0033'),  # Wacom PL600SX
    ('056a', '0034'),  # Wacom PL550
    ('056a', '0035'),  # Wacom PL800
    ('056a', '0037'),  # Wacom PL700
    ('056a', '0038'),  # Wacom PL510
    ('056a', '0039'),  # Wacom DTU-710
    ('056a', '003a'),  # Wacom DTI-520
    ('056a', '003b'),  # Wacom DTI-520
    ('056a', '003f'),  # Wacom DTZ-2100 Cintiq 21UX
    ('056a', '0041'),  # Wacom XD-0405-U Intuos2 (4x5)
    ('056a', '0042'),  # Wacom XD-0608-U Intuos2 (6x8)
    ('056a', '0043'),  # Wacom XD-0912-U Intuos2 (9x12)
    ('056a', '0044'),  # Wacom XD-1212-U Intuos2 (12x12)
    ('056a', '0045'),  # Wacom XD-1218-U Intuos2 (12x18)
    ('056a', '0057'),  # Wacom DTK-2241
    ('056a', '0059'),  # Wacom DTH-2242
    ('056a', '005b'),  # Wacom DTH-2200 Cintiq 22HD Touch
    ('056a', '005d'),  # Wacom DTH-2242
    ('056a', '005e'),  # Wacom DTH-2200 Cintiq 22HD Touch
    ('056a', '0060'),  # Wacom FT-0405 Volito, PenPartner, PenStation (4x5)
    ('056a', '0061'),  # Wacom FT-0203 Volito, PenPartner, PenStation (2x3)
    ('056a', '0062'),  # Wacom CTF-420 Volito2
    ('056a', '0063'),  # Wacom CTF-220 BizTablet
    ('056a', '0064'),  # Wacom CTF-221 PenPartner2
    ('056a', '0065'),  # Wacom MTE-450 Bamboo
    ('056a', '0069'),  # Wacom CTF-430 Bamboo One
    ('056a', '006a'),  # Wacom CTE-460 Bamboo One Pen (S)
    ('056a', '006b'),  # Wacom CTE-660 Bamboo One Pen (M)
    ('056a', '0084'),  # Wacom ACK-40401 Wireless Accessory Kit
    ('056a', '00b0'),  # Wacom PTZ-430 Intuos3 (4x5)
    ('056a', '00b1'),  # Wacom PTZ-630 Intuos3 (6x8)
    ('056a', '00b2'),  # Wacom PTZ-930 Intuos3 (9x12)
    ('056a', '00b3'),  # Wacom PTZ-1230 Intuos3 (12x12)
    ('056a', '00b4'),  # Wacom PTZ-1231W Intuos3 (12x19)
    ('056a', '00b5'),  # Wacom PTZ-631W Intuos3 (6x11)
    ('056a', '00b7'),  # Wacom PTZ-431W Intuos3 (4x6)
    ('056a', '00b8'),  # Wacom PTK-440 Intuos4 (4x6)
    ('056a', '00b9'),  # Wacom PTK-640 Intuos4 (6x9)
    ('056a', '00ba'),  # Wacom PTK-840 Intuos4 (8x13)
    ('056a', '00bb'),  # Wacom PTK-1240 Intuos4 (12x19)
    ('056a', '00bc'),  # Wacom PTK-540WL Intuos4 Wireless
    ('056a', '00c0'),  # Wacom DTF-720
    ('056a', '00c4'),  # Wacom DTF-521
    ('056a', '00c5'),  # Wacom DTZ-2000W Cintiq 20WSX
    ('056a', '00c6'),  # Wacom DTZ-1200W Cintiq 12WX
    ('056a', '00c7'),  # Wacom DTU-1931
    ('056a', '00cc'),  # Wacom DTK-2100 Cintiq 21UX
    ('056a', '00ce'),  # Wacom DTU-2231
    ('056a', '00d0'),  # Wacom CTT-460 Bamboo Touch
    ('056a', '00d1'),  # Wacom CTH-460 Bamboo Pen & Touch
    ('056a', '00d2'),  # Wacom CTH-461 Bamboo Fun/Craft/Comic Pen & Touch (S)
    ('056a', '00d3'),  # Wacom CTH-661 Bamboo Fun/Comic Pen & Touch (M)
    ('056a', '00d4'),  # Wacom CTL-460 Bamboo Pen (S)
    ('056a', '00d5'),  # Wacom CTL-660 Bamboo Pen (M)
    ('056a', '00d6'),  # Wacom CTH-460(A) Bamboo Pen & Touch
    ('056a', '00d7'),  # Wacom CTH-461(A) Bamboo Fun/Craft/Comic Pen & Touch (S)
    ('056a', '00d8'),  # Wacom CTH-661(A) Bamboo Fun/Comic Pen & Touch (M)
    ('056a', '00d9'),  # Wacom CTT-460(A) Bamboo Touch
    ('056a', '00da'),  # Wacom CTH-461SE Bamboo Pen & Touch Special Edition (S)
    ('056a', '00db'),  # Wacom CTH-661SE Bamboo Pen & Touch Special Edition (M)
    ('056a', '00dc'),  # Wacom CTT-470 Bamboo Touch
    ('056a', '00dd'),  # Wacom CTL-470 Bamboo Connect
    ('056a', '00de'),  # Wacom CTH-470 Bamboo Capture/Manga
    ('056a', '00df'),  # Wacom CTH-670 Bamboo Create/Fun
    ('056a', '00f0'),  # Wacom DTU-1631
    ('056a', '00f4'),  # Wacom DTK-2400 Cintiq 24HD
    ('056a', '00f6'),  # Wacom DTH-2400 Cintiq 24HD touch
    ('056a', '00f8'),  # Wacom DTH-2400 Cintiq 24HD touch
    ('056a', '00fa'),  # Wacom DTK-2200 Cintiq 22HD
    ('056a', '00fb'),  # Wacom DTU-1031
    ('056a', '0221'),  # Wacom MDP-123 Wacom Inkling
    ('056a', '0300'),  # Wacom CTL-471 Bamboo Splash, One by Wacom (S)
    ('056a', '0301'),  # Wacom CTL-671 One by Wacom (M)
    ('056a', '0302'),  # Wacom CTH-480 Intuos Pen & Touch (S)
    ('056a', '0303'),  # Wacom CTH-680 Intuos Pen & Touch (M)
    ('056a', '0304'),  # Wacom DTK-1300 Cintiq 13HD
    ('056a', '0304'),  # Wacom DTK-1301 Cintiq 13HD
    ('056a', '030e'),  # Wacom CTL-480 Intuos Pen (S)
    ('056a', '0314'),  # Wacom PTH-451 Intuos pro (S)
    ('056a', '0315'),  # Wacom PTH-651 Intuos pro (M)
    ('056a', '0317'),  # Wacom PTH-851 Intuos pro (L)
    ('056a', '0318'),  # Wacom CTH-301 Bamboo Pad
    ('056a', '0319'),  # Wacom CTH-300 Bamboo Pad wireless
    ('056a', '0323'),  # Wacom CTL-680 Intuos Pen (M)
    ('056a', '032a'),  # Wacom DTK-2700 Cintiq 27QHD
    ('056a', '032b'),  # Wacom DTH-2700 Cintiq 27QHD touch
    ('056a', '032c'),  # Wacom DTH-2700 Cintiq 27QHD touch
    ('056a', '032f'),  # Wacom DTU-1031X
    ('056a', '0331'),  # Wacom ACK-411050 ExpressKey Remote
    ('056a', '0333'),  # Wacom DTH-1300 Cintiq 13HD Touch
    ('056a', '0335'),  # Wacom DTH-1300 Cintiq 13HD Touch
    ('056a', '0336'),  # Wacom DTU-1141
    ('056a', '033b'),  # Wacom CTL-490 Intuos Draw small
    ('056a', '033c'),  # Wacom CTH-490 Intuos Art/Photo/Comic small
    ('056a', '033d'),  # Wacom CTL-690 Intuos Draw medium
    ('056a', '033e'),  # Wacom CTH-690 Intuos Art medium
    ('056a', '0343'),  # Wacom DTK-1651
    ('056a', '034f'),  # Wacom DTH-1320 Cintiq Pro 13
    ('056a', '0350'),  # Wacom DTH-1620 Cintiq Pro 16
    ('056a', '0351'),  # Wacom DTH-2420/DTH-2421 Cintiq Pro 24
    ('056a', '0352'),  # Wacom DTH-3220/DTH-3221 Cintiq Pro 32
    ('056a', '0353'),  # Wacom DTH-1320 Cintiq Pro 13
    ('056a', '0354'),  # Wacom DTH-1620 Cintiq Pro 16
    ('056a', '0355'),  # Wacom DTH-2420/DTH-2421 Cintiq Pro 24
    ('056a', '0356'),  # Wacom DTH-3220/DTH-3221 Cintiq Pro 32
    ('056a', '0357'),  # Wacom PTH-660 Intuos Pro medium
    ('056a', '0358'),  # Wacom PTH-860 Intuos Pro large
    ('056a', '0359'),  # Wacom DTU-1141B
    ('056a', '035A'),  # Wacom DTH-1152
    ('056a', '0368'),  # Wacom DTH-1152
    ('056a', '0374'),  # Wacom CTL-4100 Intuos S
    ('056a', '0375'),  # Wacom CTL-6100 Intuos M
    ('056a', '0376'),  # Wacom CTL-4100WL Intuos BT S
    ('056a', '0378'),  # Wacom CTL-6100WL Intuos BT M
    ('056a', '037a'),  # Wacom CTL-472 One by Wacom (s)
    ('056a', '037b'),  # Wacom CTL-672 One by Wacom (m)
    ('056a', '037c'),  # Wacom DTK-2420/DTK-2421 Cintiq Pro 24
    ('056a', '037d'),  # Wacom DTH-2452
    ('056a', '037e'),  # Wacom DTH-2452
    ('056a', '0382'),  # Wacom DTK-2451
    ('056a', '0390'),  # Wacom DTK-1660 Cintiq 16
    ('056a', '0392'),  # Wacom PTH-460 Intuos Pro Small
    ('056a', '0396'),  # Wacom DTK-1660E Cintiq 16
    ('056a', '03C0'),  # Wacom DTH271 Cintiq Pro 27
    ('056a', '03C4'),  # Wacom DTH172 Cintiq Pro 17
    ('056a', '03F0'),  # Wacom DTC135K0C Movink
    ('056a', '03a6'),  # Wacom DTC133 Wacom One Creative Pen Display
    ('056a', '03aa'),  # Wacom DTH-W1620 Mobile Studio Pro 16
    ('056a', '03ac'),  # Wacom DTH-W1620 Mobile Studio Pro 16
    ('056a', '03b2'),  # Wacom DTH167 Cintiq Pro 16
    ('056a', '03b3'),  # Wacom DTH167 Cintiq Pro 16
    ('056a', '03c5'),  # Wacom CTL-4100WL Intuos BT S
    ('056a', '03c7'),  # Wacom CTL-6100WL Intuos BT M
    ('056a', '03cb'),  # Wacom DTH134 Wacom One 13
    ('056a', '03ce'),  # Wacom DTC121 Wacom One 12
    ('056a', '03d0'),  # Wacom DTH227 Cintiq Pro 22
    ('056a', '03dc'),  # Wacom PTH-460 Intuos Pro Small
    ('056a', '03ec'),  # Wacom DTH134 DTH134
    ('056a', '03ed'),  # Wacom DTC121 DTC121

    ('09da', '054f'),  # A4 Tech Co., G7 750 mouse
    ('09da', '1410'),  # A4 Tech Co., Ltd Bloody AL9 mouse
    ('09da', '3043'),  # A4 Tech Co., Ltd Bloody R8A Gaming Mouse
    ('09da', '31b5'),  # A4 Tech Co., Ltd Bloody TL80 Terminator Laser Gaming Mouse
    ('09da', '3997'),  # A4 Tech Co., Ltd Bloody RT7 Terminator Wireless
    ('09da', '3f8b'),  # A4 Tech Co., Ltd Bloody V8 mouse
    ('09da', '51f4'),  # Modecom MC-5006 Keyboard
    ('09da', '5589'),  # A4 Tech Co., Ltd Terminator TL9 Laser Gaming Mouse
    ('09da', '7b22'),  # A4 Tech Co., Ltd Bloody V5
    ('09da', '7f2d'),  # A4 Tech Co., Ltd Bloody R3 mouse
    ('09da', '8090'),  # A4 Tech Co., Ltd X-718BK Oscar Optical Gaming Mouse
    ('09da', '9033'),  # A4 Tech Co., X7 X-705K
    ('09da', '9066'),  # A4 Tech Co., Sharkoon Fireglider Optical
    ('09da', '9090'),  # A4 Tech Co., Ltd XL-730K / XL-750BK / XL-755BK Laser Mouse
    ('09da', '90c0'),  # A4 Tech Co., Ltd X7 G800V keyboard
    ('09da', 'f012'),  # A4 Tech Co., Ltd Bloody V7 mouse
    ('09da', 'f32a'),  # A4 Tech Co., Ltd Bloody B540 keyboard
    ('09da', 'f613'),  # A4 Tech Co., Ltd Bloody V2 mouse
    ('09da', 'f624'),  # A4 Tech Co., Ltd Bloody B120 Keyboard

    ('0c45', '800a'),  # Ilebygo Mini Wireless Keyboard Mouse Touchpad Combo

    # "Speedy Industrial Supplies" mouse incorrectly named "OSA Express Network card"
    # Potentially also called "Hiraliy" or "Hiraly".
    ('1017', '2003'),

    ('16c0', '04d0'),  # Corsair STRAFE RGB Gaming Keyboard

    ('17ef', '608c'),  # LiteOn Lenovo Calliope USB Keyboard

    ('1b1c', '1b09'),  # Corsair Vengeance K70R keyboard
    ('1b1c', '1b2d'),  # Corsair Gaming K95 RGB PLATINUM Keyboard
    ('1b1c', '1b2d'),  # Corsair Gaming K95 RGB PLATINUM Keyboard
    ('1b1c', '1b2e'),  # Corsair Gaming M65 Pro RGB Mouse
    ('1b1c', '1b2e'),  # Corsair Gaming M65 Pro RGB Mouse
    ('1b1c', '1b2f'),  # Corsair Sabre RGB gaming mouse
    ('1b1c', '1b3c'),  # Corsair Harpoon RGB gaming mouse

    # August PCR450 Air Mouse/Remote
    # August PCR500 Air Mouse and Keyboard (Xenta, Freeway Technology)
    # Xenta [T3] 2.4GHz and IR Air Mouse Remote Control
    ('1d57', 'ad03'),

    ('1e7d', '2dcb'),  # Roccat Kone Pure SE(L) Mouse
    ('1e7d', '2e4a'),  # Roccat Tyon Mouse

    ('20a0', '422d'),  # Winkeyless.kr Keyboards

    ('2516', '001f'),  # Cooler Master Storm Mizar Mouse
    ('2516', '0028'),  # Cooler Master Storm Alcor Mouse

    ('26ce', '01a2'),  # ASRock LED Controller

    ('3434', '0950'),  # Keychron V5 Max System Control
]


def write_mode_0000_udev_rule_file(path, devices, message):
    filename = os.path.basename(path)
    with open(path, 'w') as f:
        f.write('# /etc/udev/rules.d/' + filename + '\n' + message + '\n')
        for vendor, product in devices:
            f.write('SUBSYSTEM=="input", ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", ENV{ID_INPUT_JOYSTICK}=="?*", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))
            f.write('SUBSYSTEM=="input", ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", KERNEL=="js[0-9]*", MODE="0000", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))


def write_rm_udev_rule_file(path, devices, message):
    filename = os.path.basename(path)
    with open(path, 'w') as f:
        f.write('# /etc/udev/rules.d/' + filename + '\n' + message + '\n')
        for vendor, product in devices:
            f.write('SUBSYSTEM=="input", ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", ENV{ID_INPUT_JOYSTICK}=="?*", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))
            f.write('SUBSYSTEM=="input", ATTRS{idVendor}=="%s", ATTRS{idProduct}=="%s", KERNEL=="js[0-9]*", RUN+="/bin/rm %%E{DEVNAME}", ENV{ID_INPUT_JOYSTICK}=""\n' % (vendor, product))


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
