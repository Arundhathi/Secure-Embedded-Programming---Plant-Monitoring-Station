import mraa

temp_raw = mraa.Aio(0)
temp_raw.setBit(12)

while(1):
    raw = temp_raw.read()
    volt = float(raw/819.0)
    C_deg = (volt * 100) - 50
    C_deg = round(C_deg,2) 
    print(C_deg)
