import re

print(
    "{'I022': 'AHMEDABAD AIRPORT', 'I032': 'AMRITSAR AIRPORT', 'I096': 'BAGDOGRA AIRPORT', 'I085': 'BENGALURU AIRPORT', 'I084': 'BHUBANESHWAR AIRPORT', 'I010': 'CALICUT AIRPORT', 'I005': 'CHANDIGARH AIRPORT', 'I008': 'CHENNAI AIRPORT', 'I024': 'COCHIN AIRPORT', 'I094': 'COIMBATORE AIRPORT', 'I004': 'DELHI AIRPORT', 'I012': 'GAYA AIRPORT', 'I019': 'GUWAHATI AIRPORT', 'I041': 'HYDERABAD AIRPORT', 'I017': 'INDORE AIRPORT', 'I006': 'JAIPUR AIRPORT', 'I030': 'KANNUR AIRPORT', 'I002': 'KOLKATA AIRPORT', 'I021': 'LUCKNOW AIRPORT', 'I015': 'MADURAI AIRPORT', 'I092': 'MANGALORE AIRPORT', 'I001': 'MUMBAI AIRPORT', 'I016': 'NAGPUR AIRPORT', 'I077': 'PORTBLAIR AIRPORT', 'I026': 'PUNE AIRPORT', 'I003': 'TIRUCHIRAPALLI AIRPORT', 'I023': 'TRIVANDRUM AIRPORT', 'I007': 'VARANASI AIRPORT', 'I025': 'VISHAKHAPATNAM AIRPORT'}".replace(
        "'", '"'
    )
)
with open("./temp.txt", "r") as f:
    result = {}
    for line in f.readlines():
        if len(line) == "\n":
            continue
        values = re.match(r"<option  value='(I0\d{2})'>([A-Z\s]+)</option>", line)
        if values:
            result[values.group(1)] = values.group(2)
    print(result)
