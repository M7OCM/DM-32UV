# DM-32UV
Baofeng firmware for the DM-32UV DMR radio the most common type sold in China via Aliexpress, Banggood etc. Firmware always begins with 01. If installed on the wrong hardware (ie the HR Vocoder version) it will soft brick the radio, solution is to remove battery, turn device on while pressing SK1 and PTT (reattach battery) and reflash the correct version.

Reset radio by first uploading a CPS file with allow reset selected and turn on while holding SK1 and SK2, the reset menu can then be initialised.

As of late 2025 DM32.01.01.047 or DM32.01.01.049 firmware has been appearing on newly sold radios.

The bin files containing NRF and Fanti are sourced from Taiwan for the FT-399DMR/DM-32 [rowa.com.tw](https://www.rowa.com.tw/store/index.php?route=product/product&path=134&product_id=1731)

## Flash dump
The zip file contains Open UV008 a program to extract firmware from the Baofeng DM-32UV (and obviously the Zastone UV008). Before running enter the ini file and amend the file location to your setup, save, exit.

To extract the flash dump for the DM-32UV select *GD25Q16* (read/write SPI flash), select correct COM port of radio. **Turn off radio**, save as (name/location of completed dump) press read and the process will begin. It takes a while but leave it to finish. You can forward the file (zip file only not raw binary) to me directly - just get in touch through the discussion option it can then be converted to a useable bin file for upload here.
