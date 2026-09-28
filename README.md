# DM-32UV
A few examples of modded firmware files for the common version of the DM-32UV care of the multi talented radio ham RA4FHE at [infotex58.ru](http://infotex58.ru/forum/index.php?topic=1148.0)

Extended frequency ranges do not mean the radio will receive or transmit outside of the original spec due to hardware constraints, filtering etc and may damage your radio if used without hardware modification.

The latest firmware mod has inverted screen colour, a white background useful for outdoor use. Bear in mind the start up picture will also be inverted so use Gimp or Photoshop to invert images prior to upload.

## GPS / APRS NMEA padding fix for 01.L01.048

`DM32.01.L01.048_GPS-NMEA-padding-fix.bin` fixes malformed GPS longitude formatting observed in firmware `01.L01.048`, where longitudes requiring leading zeroes could be emitted as an invalid NMEA field (for example `742.1234\0\0,E` instead of `00742.1234,E`). The values in this example are synthetic and do not represent the real test location.

The fix has been tested on real hardware with BrandMeister and APRS.fi. Full technical analysis, offsets, checksums and reproduction steps are in [`GPS_NMEA_PADDING_FIX_01.L01.048.md`](GPS_NMEA_PADDING_FIX_01.L01.048.md). A reproducible patch script is also included as [`make_gps_nmea_padding_fix.py`](make_gps_nmea_padding_fix.py).

GPS/APRS padding fix research, testing and patch: **IU2VTP**.

Use with caution and informed risk, you decide.
