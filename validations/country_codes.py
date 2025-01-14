#Will be useful in data_validation - might later be in a json file
class CountryCodes:
    def __init__(self):
        self.country_codes = country_codes = {
                        44: "United Kingdom",
                        33: "France",
                        49: "Germany",
                        81: "Japan",
                        86: "China",
                        91: "India",
                        7: "Russia",
                        93: "Afghanistan",
                        355: "Albania",
                        376: "Andorra",
                        244: "Angola",
                        54: "Argentina",
                        374: "Armenia",
                        297: "Aruba",
                        61: "Australia",
                        43: "Austria",
                        994: "Azerbaijan",
                        973: "Bahrain",
                        880: "Bangladesh",
                        375: "Belarus",
                        32: "Belgium",
                        501: "Belize",
                        229: "Benin",
                        975: "Bhutan",
                        591: "Bolivia",
                        387: "Bosnia and Herzegovina",
                        267: "Botswana",
                        55: "Brazil",
                        673: "Brunei",
                        359: "Bulgaria",
                        226: "Burkina Faso",
                        257: "Burundi",
                        855: "Cambodia",
                        1: "Canada",
                        56: "Chile",
                        57: "Colombia",
                        506: "Costa Rica",
                        385: "Croatia",
                        53: "Cuba",
                        213: "Algeria",
                        237: "Cameroon",
                        238: "Cape Verde",
                        236: "Central African Republic",
                        235: "Chad",
                        269: "Comoros",
                        242: "Congo, Republic of the",
                        243: "Congo, Democratic Republic of the",
                        253: "Djibouti",
                        20: "Egypt",
                        240: "Equatorial Guinea",
                        291: "Eritrea",
                        251: "Ethiopia",
                        220: "Gambia",
                        233: "Ghana",
                        224: "Guinea",
                        245: "Guinea-Bissau",
                        254: "Kenya",
                        266: "Lesotho",
                        231: "Liberia",
                        218: "Libya",
                        261: "Madagascar",
                        265: "Malawi",
                        223: "Mali",
                        222: "Mauritania",
                        230: "Mauritius",
                        258: "Mozambique",
                        264: "Namibia",
                        227: "Niger",
                        234: "Nigeria",
                        250: "Rwanda",
                        290: "Saint Helena",
                        239: "São Tomé and Príncipe",
                        221: "Senegal",
                        248: "Seychelles",
                        232: "Sierra Leone",
                        252: "Somalia",
                        27: "South Africa",
                        211: "South Sudan",
                        249: "Sudan",
                        268: "Swaziland",
                        255: "Tanzania",
                        228: "Togo",
                        216: "Tunisia",
                        256: "Uganda",
                        212: "Western Sahara",
                        260: "Zambia",
                        263: "Zimbabwe"
                    }

    def get_country_by_code(self, code):
        return self.country_codes.get(code, "Unknown")

country_codes = CountryCodes()
get_country_by_code = country_codes.get_country_by_code
