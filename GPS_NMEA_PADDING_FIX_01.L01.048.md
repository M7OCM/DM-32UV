# DM-32UV GPS / APRS NMEA padding fix — firmware 01.L01.048

## Summary

This patch fixes malformed NMEA RMC longitude formatting observed on a Baofeng DM-32UV running firmware `DM32.01.L01.048` when sending GPS/APRS data over DMR to BrandMeister.

The bug was observed on real hardware and reproduced in packet captures. The exact test coordinates are intentionally omitted. A sanitized example of the malformed longitude field is:

```text
742.1234\0\0,E
```

instead of the NMEA-compliant representation:

```text
00742.1234,E
```

BrandMeister received the complete DMR data transmission but did not publish the position to APRS-IS / APRS.fi. After applying the patch, the radio transmitted the correctly zero-padded longitude and the position was successfully published by BrandMeister to APRS.fi.

## Tested setup

- Radio: Baofeng DM-32UV
- Base firmware: `DM32.01.L01.048.bin`
- GPS/APRS: fixed/manual beacon during debugging, then verified end-to-end
- DMR destination: `222999`
- Call type: Private
- SMS format: M-SMS
- BrandMeister SelfCare radio brand: Motorola
- Hotspot path: MMDVMHost → DMRGateway → BrandMeister

The DMR transport itself was verified independently. Packet captures showed complete outbound `DMRD` frames and DMRGateway rule tracing showed the private-data rule matching correctly. The malformed coordinate therefore originated in the radio payload rather than in DMRGateway.

## What was seen on the air

The reconstructed RMC payload before patching had the same structure as this sanitized example:

```text
$GPRMC,...,1234.5678,N,742.1234\0\0,E,0.00,0.00,...
```

For a longitude of 7°42.1234′ E, NMEA requires longitude in `dddmm.mmmm` form:

```text
00742.1234,E
```

The values above are deliberately synthetic and are not the coordinates used during the real test.

The stock firmware kept a fixed-width field but left two trailing NUL bytes instead of adding the required leading zeroes.

## Firmware analysis

The firmware contains floating-point format strings used by the GPS/NMEA code:

```text
%04.4f
%05.4f
```

In `printf`-style formatting, the number before `.4f` is the minimum total field width, not the number of digits before the decimal point. Therefore `%05.4f` does not pad a value such as `742.1234`, because that string is already wider than five characters.

NMEA latitude `ddmm.mmmm` needs a 9-character numeric field, while longitude `dddmm.mmmm` needs a 10-character numeric field. Adding the `0` flag makes the padding occur on the left.

## Patch

Two format strings are changed, preserving the firmware size:

```text
Offset 0x0A94F8
%04.4f  ->  %09.4f

Offset 0x0A9500
%05.4f\0\0  ->  %010.4f\0
```

Only 6 bytes differ between the original and patched image.

The intended effect is:

```text
742.1234   -> 00742.1234
```

and, similarly, correct left zero-padding for latitude when required.

## Checksums

Original `DM32.01.L01.048.bin`:

```text
SHA256 fda860febfcf1a234eed7fa73272112891074aac83746e4f8dfe224a2a700f8f
```

Patched `DM32.01.L01.048_GPS-NMEA-padding-fix.bin`:

```text
SHA256 e138c4740cb8c93910e03b1172fbf1d94fb80cd6241d9c1cda764d1736634075
```

Patched image size: `860416` bytes.

## Validation

The patch was flashed to a real DM-32UV and tested with the same real-world position that previously failed. The actual coordinates are intentionally not included in this repository.

Before patching, BrandMeister received the DMR data but no APRS.fi position appeared. After patching, the radio generated the correctly padded longitude and BrandMeister successfully published the position to APRS.fi.

This confirms the fix end-to-end on the tested `01.L01.048` firmware/hardware combination.

## Reproducing the binary patch

The included `make_gps_nmea_padding_fix.py` script reproduces the binary change from a known-good original firmware image and refuses to patch if the SHA256 does not match the tested base firmware.

## Credits

Research, reverse-engineering, hardware testing and patch: **IU2VTP**.

## Scope and cautions

This was tested on firmware `01.L01.048`. Do not assume the same offsets are valid for another firmware revision.

This is an unofficial firmware modification. Flashing modified firmware always carries a risk of making the radio unusable. Keep a known-good original firmware image available for recovery and verify hashes before flashing.
