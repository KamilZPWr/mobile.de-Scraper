A1 = 'A1'
AUDI = 'audi'
SUB_CODES = 'sub_codes'
GENERAL_CODE = 'general_code'
BRAND_TYPES = 'brand_types'
BRAND_CODE = 'brand_code'
CHROME_DRIVER_PATH = "/Users/ag283qj/code/scraper/chromedriver"


CAR_BRANDS = {
    AUDI: {
            BRAND_CODE: 1900,
            BRAND_TYPES: {
                '100': 2,
                '200': 3,
                '80': 5,
                '90': 6,
                A1: 25,
                'A2': 7,
                'A3': 8,
                'A4': 9,
                'A4 Allroad': 33,
                'A5': 31,
                'A6': 10,
                'A6 Allroad': 12,
                'A7': 34,
                'A8': 11,
                'Q1': 43,
                'Q2': 45,
                'Q3': 37,
                'Q5': 32,
                'Q7': 15,
                'Q8': 46,
                'R8': 29,
                'RS2': 26,
                'RS3': 36,
                'RS4': 27,
                'RS5': 17,
                'RS6': 28,
                'RS7': 40,
                'RSQ3': 41,
                'RSQ8': 55,
                'S1': 42,
                'S2': 18,
                'S3': 19,
                'S4': 20,
                'S5': 30,
                'S6': 21,
                'S7': 38,
                'S8': 22,
                'SQ2': 47,
                'SQ5': 39,
                'SQ7': 44,
                'SQ8': 54,
                'TT': 23,
                'TT RS': 35,
                'TTS': 4,
                'V8': 24
            }
    },
    'bmw': {
        BRAND_CODE: 3500,
        BRAND_TYPES: {
            'Series 1': {
                GENERAL_CODE: ';20',
                SUB_CODES: {
                    '114': 73,
                    '116': 2,
                    '118': 3,
                    '120': 4,
                    '123': 59,
                    '125': 61,
                    '130': 5,
                    '135': 58
                }
            },
            'Series 2': {
                GENERAL_CODE: ';55',
                SUB_CODES: {
                    '214 Active Tourer': 110,
                    '214 Gran Tourer': 116,
                    '216': 106,
                    '216 Active Tourer': 111,
                    '216 Gran Tourer': 114,
                    '218': 90,
                    '218 Active Tourer': 107,
                    '218 Gran Tourer': 112,
                    '220': 84,
                    '220 Active Tourer': 108,
                    '220 Gran Tourer': 113,
                    '225': 91,
                    '225 Active Tourer': 109,
                    '228': 104,
                    '230': 125,
                }
            },
            'Series 3': {
                GENERAL_CODE: ';21',
                SUB_CODES: {
                    '315': 7,
                    '316': 8,
                    '318': 9,
                    '318 Gran Turismo': 75,
                    '320': 10,
                    '320 Gran Turismo': 76,
                    '323': 11,
                    '324': 12,
                    '325': 13,
                    '325 Gran Turismo': 88,
                    '328': 14,
                    '328 Gran Turismo': 77,
                    '330': 15,
                    '330 Gran Turismo': 103,
                    '335': 56,
                    '335 Gran Turismo': 78,
                    '340': 118,
                    '340 Gran Turismo': 130,
                }
            },
            'Series 4': {
                GENERAL_CODE: ';53',
                SUB_CODES: {
                    '418': 115,
                    '418 Gran Coupe': 98,
                    '420': 80,
                    '420 Gran Coupe': 99,
                    '425': 102,
                    '425 Gran Coupe': 124,
                    '428': 81,
                    '428 Gran Coupe': 100,
                    '430': 83,
                    '430 Gran Coupe': 105,
                    '435': 82,
                    '435 Gran Coupe': 101,
                    '440': 120,
                    '440 Gran Coupe': 121,
                }
            },
        },
    },
    'ford': {
        BRAND_CODE: 9000,
        BRAND_TYPES: {
            'B-Max': 54,
            'C-Max': 52,
            'EcoSport': 56,
            'Edge': 48,
            'Fiesta': 19,
            'Focus': 20,
            'Fusion': 22,
            'Galaxy': 23,
            'Ka/Ka+': 25,
            'Kuga': 49,
            'Mondeo': 29,
            'S-Max': 47,
        },
    },
    'mercedes-benz': {
        BRAND_CODE: 17200,
        BRAND_TYPES: {
            'Class A': {
                GENERAL_CODE: ';4',
                SUB_CODES: {
                    'A140': 2,
                    'A150': 3,
                    'A160': 4,
                    'A170': 5,
                    'A180': 6,
                    'A190': 7,
                    'A200': 8,
                    'A210': 9,
                    'A220': 221,
                    'A250': 220,
                }
            },
            'Class B': {
                GENERAL_CODE: ';5',
                SUB_CODES: {
                    'B150': 12,
                    'B160': 11,
                    'B170': 13,
                    'B180': 14,
                    'B200': 15,
                    'B220': 222,
                    'B250': 223,
                }
            },
            'Class C': {
                GENERAL_CODE: ';6',
                SUB_CODES: {
                    'C160': 16,
                    'C180': 17,
                    'C200': 18,
                    'C220': 19,
                    'C230': 20,
                    'C240': 21,
                    'C250': 22,
                    'C270': 23,
                    'C280': 24,
                    'C300': 44,
                    'C30 AMG': 25,
                    'C320': 27,
                    'C32 AMG': 26,
                    'C350': 28,
                    'C36 AMG': 29,
                    'C400': 245,
                    'C43 AMG': 30,
                    'C450 AMG': 246,
                    'C55 AMG': 31,
                    'C63 AMG': 198
                }
            },
        }
    },
    'opel': {
        BRAND_CODE: 19000,
        BRAND_TYPES: {
            'Adam': 38,
            'Agila': 2,
            'Astra': 5,
            'Combo': 8,
            'Corsa': 10,
            'Insignia': 35,
            'Karl': 41,
            'Meriva': 16,
            'Mokka': 37,
            'Mokka X': 44,
            'Signum': 24,
            'Vectra': 29,
            'Vivaro': 30,
            'Zafira': 31
        }
    },
    'skoda': {
        BRAND_CODE: 22900,
        BRAND_TYPES: {
            'Citigo': 17,
            'Fabia': 6,
            'Kamiq': 24,
            'Karoq': 20,
            'Kodiaq': 19,
            'Octavia': 10,
            'Rapid': 18,
            'Roomster': 13,
            'Scala': 21,
            'Superb': 12,
            'Yeti': 15,
        }
    },
    'toyota': {
        BRAND_CODE: 24100,
        BRAND_TYPES: {
            'auris': 39,

        }
    },
    'volkswagen': 25200,
    'alfa romeo': 900,
    'chevrolet': 5600,
    'citroen': 5900,
    'dacia': 6600,
    'fiat': 8800,
    'honda': 11000,
    'hyundai': 11600,
    'kia': 13200,
    'mazda': 16800,
    'nissan': 18700,
    'peugeot': 19300,
    'renault': 20700,
    'seat': 22500,
    'suzuki': 23600,
    'volvo': 25100
}

