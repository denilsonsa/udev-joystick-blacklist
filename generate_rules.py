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

    ('3233', '0009'),  # Ducky Feather mouse
    ('3233', '000b'),  # Ducky Secret M Retro mouse
    ('3233', '000d'),  # Ducky One 3 Pro RGB mouse
    ('3233', '000f'),  # Ducky 75% ANSI keyboard
    ('3233', '0015'),  # Ducky One 3 Pro Mini RGB mouse
    ('3233', '0019'),  # Ducky One X Wireless keyboard
    ('3233', '001a'),  # Ducky One X 2.4GHz
    ('3233', '001d'),  # Ducky One X Mini Wireless keyboard
    ('3233', '1011'),  # Ducky One 3 mouse
    ('3233', '1012'),  # Ducky Origin keyboard
    ('3233', '1311'),  # Ducky One 3 RGB keyboard
    ('3233', '1311'),  # Ducky One 3 RGB keyboard
    ('3233', '5311'),  # Ducky One 3 SF RGB keyboard
    ('3233', '6301'),  # Ducky One2 Mini RGB keyboard
    ('3233', '6311'),  # Ducky One 3 Mini RGB keyboard
    ('3233', '8011'),  # Ducky One 3 TKL keyboard
    ('3233', '8311'),  # Ducky One 3 TKL RGB keyboard

    ('3434', '0100'),  # Keychron Q1 keyboard
    ('3434', '0101'),  # Keychron Q1 mouse
    ('3434', '0102'),  # Keychron Q1 keyboard
    ('3434', '0106'),  # Keychron Q1 keyboard
    ('3434', '0107'),  # Keychron Q1 keyboard
    ('3434', '0109'),  # Keychron Q1 keyboard
    ('3434', '010b'),  # Keychron Q1 keyboard
    ('3434', '0110'),  # Keychron Q2 keyboard
    ('3434', '0111'),  # Keychron Q2 mouse
    ('3434', '0113'),  # Keychron Q2 mouse
    ('3434', '0120'),  # Keychron Q3 keyboard
    ('3434', '0121'),  # Keychron Q3 mouse
    ('3434', '0123'),  # Keychron Q3 mouse
    ('3434', '0130'),  # Keychron Q0 keyboard
    ('3434', '0131'),  # Keychron Q0 Plus mouse
    ('3434', '0140'),  # Keychron Q4 mouse
    ('3434', '0142'),  # Keychron Q4 keyboard
    ('3434', '0150'),  # Keychron Q5 keyboard
    ('3434', '0151'),  # Keychron Q5 mouse
    ('3434', '0153'),  # Keychron Q5 keyboard
    ('3434', '0160'),  # Keychron Q6 keyboard
    ('3434', '0161'),  # Keychron Q6 keyboard
    ('3434', '0163'),  # Keychron Q6 keyboard
    ('3434', '0172'),  # Keychron Q7 keyboard
    ('3434', '0180'),  # Keychron Q8 keyboard
    ('3434', '0181'),  # Keychron Q8 keyboard
    ('3434', '0182'),  # Keychron Q8 mouse
    ('3434', '0183'),  # Keychron Q8 keyboard
    ('3434', '0190'),  # Keychron Q9 keyboard
    ('3434', '01a1'),  # Keychron Q10 mouse
    ('3434', '01a3'),  # Keychron Q10 keyboard
    ('3434', '01b1'),  # Keychron Q65 mouse
    ('3434', '01d1'),  # Keychron Q12 keyboard
    ('3434', '01e0'),  # Keychron Q11 keyboard
    ('3434', '01e1'),  # Keychron Q11 mouse
    ('3434', '0206'),  # Keychron K17 Pro keyboard
    ('3434', '0207'),  # Keychron K17 Pro keyboard
    ('3434', '0210'),  # Keychron K1 Pro mouse
    ('3434', '0211'),  # Keychron K1 Pro keyboard
    ('3434', '0213'),  # Keychron K1 Pro mouse
    ('3434', '0220'),  # Keychron K2 Pro mouse
    ('3434', '0221'),  # Keychron K2 Pro mouse
    ('3434', '0223'),  # Keychron K2 Pro keyboard
    ('3434', '0230'),  # Keychron K3 Pro mouse
    ('3434', '0231'),  # Keychron K3 Pro mouse
    ('3434', '0233'),  # Keychron K3 Pro keyboard
    ('3434', '0234'),  # Keychron K3 Pro mouse
    ('3434', '0240'),  # Keychron K4 Pro keyboard
    ('3434', '0241'),  # Keychron K4 Pro keyboard
    ('3434', '0243'),  # Keychron K4 Pro keyboard
    ('3434', '0245'),  # Keychron K4 Pro mouse
    ('3434', '0250'),  # Keychron K5 Pro mouse
    ('3434', '0251'),  # Keychron K5 Pro keyboard
    ('3434', '0253'),  # Keychron K5 Pro keyboard
    ('3434', '0260'),  # Keychron K6 Pro keyboard
    ('3434', '0263'),  # Keychron K6 Pro keyboard
    ('3434', '0270'),  # Keychron K7 Pro mouse
    ('3434', '0273'),  # Keychron K7 Pro keyboard
    ('3434', '0280'),  # Keychron K8 Pro keyboard
    ('3434', '0281'),  # Keychron K8 Pro keyboard
    ('3434', '0283'),  # Keychron K8 Pro mouse
    ('3434', '0284'),  # Keychron K8 Pro keyboard
    ('3434', '0290'),  # Keychron K9 Pro keyboard
    ('3434', '0293'),  # Keychron K9 Pro keyboard
    ('3434', '02a0'),  # Keychron K10 Pro keyboard
    ('3434', '02a1'),  # Keychron K10 Pro mouse
    ('3434', '02a3'),  # Keychron K10 Pro mouse
    ('3434', '02a4'),  # Keychron K10 Pro mouse
    ('3434', '02b6'),  # Keychron K11 Pro mouse
    ('3434', '02b9'),  # Keychron K11 Pro keyboard
    ('3434', '02d0'),  # Keychron K13 Pro mouse
    ('3434', '02d1'),  # Keychron K13 Pro keyboard
    ('3434', '02d3'),  # Keychron K13 Pro keyboard
    ('3434', '02f6'),  # Keychron K15 Pro mouse
    ('3434', '0310'),  # Keychron V1 mouse
    ('3434', '0311'),  # Keychron V1 mouse
    ('3434', '0313'),  # Keychron V1 keyboard
    ('3434', '0321'),  # Keychron V2 mouse
    ('3434', '0330'),  # Keychron V3 keyboard
    ('3434', '0331'),  # Keychron V3 keyboard
    ('3434', '0333'),  # Keychron V3 keyboard
    ('3434', '0340'),  # Keychron V4 keyboard
    ('3434', '0342'),  # Keychron V4 mouse
    ('3434', '0350'),  # Keychron V5 keyboard
    ('3434', '0351'),  # Keychron V5 keyboard
    ('3434', '0353'),  # Keychron V5 mouse
    ('3434', '0360'),  # Keychron V6 keyboard
    ('3434', '0361'),  # Keychron V6 mouse
    ('3434', '0363'),  # Keychron V6 keyboard
    ('3434', '03a1'),  # Keychron V10 mouse
    ('3434', '03a3'),  # Keychron V10 keyboard
    ('3434', '0410'),  # Keychron S1 keyboard
    ('3434', '0411'),  # Keychron S1 keyboard
    ('3434', '0430'),  # Keychron C3 Pro mouse
    ('3434', '0431'),  # Keychron C3 Pro mouse
    ('3434', '0433'),  # Keychron C3 Pro keyboard
    ('3434', '0434'),  # Keychron C3 Pro mouse
    ('3434', '0437'),  # Keychron C3 Pro 8K keyboard
    ('3434', '0500'),  # Keychron M1 Mouse mouse
    ('3434', '0510'),  # Keychron C1 Pro mouse
    ('3434', '0526'),  # Keychron C2 Pro mouse
    ('3434', '0529'),  # Keychron C2 Pro keyboard
    ('3434', '0610'),  # Keychron Q1 Pro keyboard
    ('3434', '0611'),  # Keychron Q1 Pro keyboard
    ('3434', '0620'),  # Keychron Q2 Pro keyboard
    ('3434', '0621'),  # Keychron Q2 Pro keyboard
    ('3434', '0630'),  # Keychron Q3 Pro mouse
    ('3434', '0631'),  # Keychron Q3 Pro keyboard
    ('3434', '0650'),  # Keychron Q5 Pro keyboard
    ('3434', '0660'),  # Keychron Q6 Pro mouse
    ('3434', '0661'),  # Keychron Q6 Pro mouse
    ('3434', '0680'),  # Keychron Q8 Pro mouse
    ('3434', '06a0'),  # Keychron Q10 Pro keyboard
    ('3434', '06d0'),  # Keychron Q13 Pro keyboard
    ('3434', '0711'),  # Keychron B1 Pro mouse
    ('3434', '0761'),  # Keychron B6 Pro keyboard
    ('3434', '07f0'),  # Keychron B33 keyboard
    ('3434', '0800'),  # Keychron Q0 Max mouse
    ('3434', '0810'),  # Keychron Q1 Max keyboard
    ('3434', '0811'),  # Keychron Q1 Max keyboard
    ('3434', '0820'),  # Keychron Q2 Max keyboard
    ('3434', '0830'),  # Keychron Q3 Max keyboard
    ('3434', '0831'),  # Keychron Q3 Max mouse
    ('3434', '0850'),  # Keychron Q5 Max mouse
    ('3434', '0851'),  # Keychron Q5 Max mouse
    ('3434', '0860'),  # Keychron Q6 Max keyboard
    ('3434', '0861'),  # Keychron Q6 Max mouse
    ('3434', '08c0'),  # Keychron Q60 Max keyboard
    ('3434', '08c3'),  # Keychron Q12 Max keyboard
    ('3434', '08d0'),  # Keychron Q13 Max keyboard
    ('3434', '08f0'),  # Keychron Q15 Max mouse
    ('3434', '0913'),  # Keychron V1 Max mouse
    ('3434', '0914'),  # Keychron V1 Max mouse
    ('3434', '0933'),  # Keychron V3 Max mouse
    ('3434', '0934'),  # Keychron V3 Max keyboard
    ('3434', '0950'),  # Keychron V5 Max keyboard
    ('3434', '0951'),  # Keychron V5 Max keyboard
    ('3434', '0960'),  # Keychron V6 Max mouse
    ('3434', '0961'),  # Keychron V6 Max keyboard
    ('3434', '09a0'),  # Keychron V10 Max mouse
    ('3434', '0a03'),  # Keychron K17 Max mouse
    ('3434', '0a04'),  # Keychron K17 Max mouse
    ('3434', '0a06'),  # Keychron K0 Max keyboard
    ('3434', '0a10'),  # Keychron K1 Max keyboard
    ('3434', '0a30'),  # Keychron K3 Max mouse
    ('3434', '0a31'),  # Keychron K3 Max keyboard
    ('3434', '0a32'),  # Keychron K3 Max keyboard
    ('3434', '0a33'),  # Keychron K3 Max keyboard
    ('3434', '0a38'),  # Keychron K3 Max mouse
    ('3434', '0a50'),  # Keychron K5 Max mouse
    ('3434', '0a51'),  # Keychron K5 Max keyboard
    ('3434', '0a53'),  # Keychron K5 Max keyboard
    ('3434', '0a70'),  # Keychron K7 Max mouse
    ('3434', '0a80'),  # Keychron K8 Max keyboard
    ('3434', '0aa0'),  # Keychron K10 Max mouse
    ('3434', '0aa1'),  # Keychron K10 Max keyboard
    ('3434', '0ab3'),  # Keychron K11 Max mouse
    ('3434', '0ad0'),  # Keychron K13 Max keyboard
    ('3434', '0af3'),  # Keychron K15 Max mouse
    ('3434', '0b10'),  # Keychron Q1 HE keyboard
    ('3434', '0b11'),  # Keychron Q1 HE keyboard
    ('3434', '0b30'),  # Keychron Q3 HE keyboard
    ('3434', '0b60'),  # Keychron Q6 HE keyboard
    ('3434', '0d10'),  # Keychron K1 Version 6 keyboard
    ('3434', '0d20'),  # Keychron K2 Version 3 mouse
    ('3434', '0d23'),  # Keychron K2 Version 3 keyboard
    ('3434', '0d30'),  # Keychron K3 Version 3 mouse
    ('3434', '0d31'),  # Keychron K3 Version 3 mouse
    ('3434', '0d33'),  # Keychron K3 Version 3 keyboard
    ('3434', '0d34'),  # Keychron K3 Version 3 mouse
    ('3434', '0d50'),  # Keychron K5 Version 2 keyboard
    ('3434', '0d51'),  # Keychron K5 Version 2 mouse
    ('3434', '0d80'),  # Keychron K8 Version 2 mouse
    ('3434', '0da0'),  # Keychron K10 Version 2 mouse
    ('3434', '0da1'),  # Keychron K10 Version 2 mouse
    ('3434', '0da3'),  # Keychron K10 Version 2 keyboard
    ('3434', '0e20'),  # Keychron K2 HE keyboard
    ('3434', '0e21'),  # Keychron K2 HE keyboard
    ('3434', '0e40'),  # Keychron K4 HE keyboard
    ('3434', '0ea0'),  # Keychron K10 HE keyboard
    ('3434', '11a3'),  # Keychron K10 keyboard
    ('3434', 'd026'),  # Keychron Link-KM keyboard
    ('3434', 'd027'),  # Keychron Receiver keyboard
    ('3434', 'd028'),  # Keychron Ultra-Link 8K mouse
    ('3434', 'd030'),  # Keychron Link keyboard
    ('3434', 'd031'),  # Keychron Link keyboard
    ('3434', 'd033'),  # Keychron M3 keyboard
    ('3434', 'd035'),  # Keychron M1 mouse
    ('3434', 'd036'),  # Keychron M3 mini mouse
    ('3434', 'd038'),  # Keychron 4K Link mouse
    ('3434', 'd03f'),  # Keychron M6 mouse
    ('3434', 'd040'),  # Keychron M4 mouse
    ('3434', 'd041'),  # Keychron M3 mini 4K mouse
    ('3434', 'd044'),  # Keychron M7 mouse
    ('3434', 'd045'),  # Keychron M2 4K mouse
    ('3434', 'd046'),  # Keychron M6 4K mouse
    ('3434', 'd048'),  # Keychron M5 8K keyboard
    ('3434', 'd049'),  # Keychron M6 8K keyboard
    ('3434', 'd04c'),  # Keychron M3 mouse
    ('3434', 'd04e'),  # Keychron M3 keyboard
    ('3434', 'd060'),  # Keychron M6 keyboard
    ('3434', 'fe06'),  # Keychron K4v2 RGB keyboard
    ('3434', 'fe0a'),  # Keychron K6 RGB keyboard
    ('3434', 'fe0e'),  # Keychron K8 RGB keyboard
    ('3434', 'fe0f'),  # Keychron K8 RGB keyboard
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
