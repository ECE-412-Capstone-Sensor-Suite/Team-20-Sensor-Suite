cd %~dp0
ESP -E
ESP -P FT-DC9018B-MOTE-M4-115K-680-0380-0002REV1.bin 0
ESP -P mote_part_r52074.bin 800
cd C:\Users\Yesoooof\Documents\GitHub\Team-20-Sensor-Suite\Firmware\On-chip App\onchipsdk-master\projects\iar\02-i2c\Debug\Exe
ESP -P ocfdk_02_i2c.bin 1000
cd %~dp0
ESP -P loader_1_0_6_4_oski.bin 77800