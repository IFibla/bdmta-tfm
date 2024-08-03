from enum import Enum
from typing import Dict

class NationalityId(Enum):
    AMERICAN = 1
    ARGENTINEAN = 2
    AUSTRALIAN = 3
    AUSTRIAN = 4
    AZERBAIJANI = 5
    BAHRAINI = 6
    BELGIAN = 7
    BOLIVIAN = 8
    BRAZILIAN = 9
    BRITISH = 10
    BULGARIAN = 11
    CAMEROONIAN = 12
    CANADIAN = 13
    CHILEAN = 14
    CHINESE = 15
    COLOMBIAN = 16
    COSTA_RICAN = 17
    CROATIAN = 18
    CYPRIOT = 19
    CZECH = 20
    DANISH = 21
    DUTCH = 22
    ECUADORIAN = 23
    ENGLISH = 24
    EMIRIAN = 25
    ESTONIAN = 26
    FINNISH = 27
    FRENCH = 28
    GERMAN = 29
    GHANAIAN = 30
    GREEK = 31
    GUATEMALAN = 32
    HONDURAN = 33
    HONG_KONGER = 34
    HUNGARIAN = 35
    ICELANDER = 36
    INDIAN = 37
    INDONESIAN = 38
    IRISH = 39
    ISRAELI = 40
    ITALIAN = 41
    JAMAICAN = 42
    JAPANESE = 43
    JORDANIAN = 44
    KUWAITI = 45
    LATVIAN = 46
    LEBANESE = 47
    LITHUANIAN = 48
    LUXEMBOURGER = 49
    MALAYSIAN = 50
    MALTESE = 51
    MEXICAN = 52
    MONEGASQUE = 53
    NEW_ZEALANDER = 54
    NICARAGUAN = 55
    NORTHERN_IRISH = 56
    NORWEGIAN = 57
    OMANI = 58
    PAKISTANI = 59
    PANAMANIAN = 60
    PARAGUAYAN = 61
    PERUVIAN = 62
    POLISH = 63
    PORTUGUESE = 64
    QATARI = 65
    ROMANIAN = 66
    RUSSIAN = 67
    SALVADORAN = 68
    SAUDI = 69
    SCOTTISH = 70
    SERBIAN = 71
    SINGAPOREAN = 72
    SLOVAKIAN = 73
    SLOVENIAN = 74
    SOUTH_KOREAN = 75
    SOUTH_AFRICAN = 76
    SPANISH = 77
    SWEDISH = 78
    SWISS = 79
    THAI = 80
    TURKISH = 81
    URUGUAYAN = 82
    UKRAINIAN = 83
    VENEZUELAN = 84
    BARBADIAN = 85
    WELSH = 86
    VIETNAMESE = 87

NATIONALITY_NAMES: Dict[int, str] = {
    NationalityId.AMERICAN.value: "American",
    NationalityId.ARGENTINEAN.value: "Argentinean",
    NationalityId.AUSTRALIAN.value: "Australian",
    NationalityId.AUSTRIAN.value: "Austrian",
    NationalityId.AZERBAIJANI.value: "Azerbaijani",
    NationalityId.BAHRAINI.value: "Bahraini",
    NationalityId.BELGIAN.value: "Belgian",
    NationalityId.BOLIVIAN.value: "Bolivian",
    NationalityId.BRAZILIAN.value: "Brazilian",
    NationalityId.BRITISH.value: "British",
    NationalityId.BULGARIAN.value: "Bulgarian",
    NationalityId.CAMEROONIAN.value: "Cameroonian",
    NationalityId.CANADIAN.value: "Canadian",
    NationalityId.CHILEAN.value: "Chilean",
    NationalityId.CHINESE.value: "Chinese",
    NationalityId.COLOMBIAN.value: "Colombian",
    NationalityId.COSTA_RICAN.value: "Costa Rican",
    NationalityId.CROATIAN.value: "Croatian",
    NationalityId.CYPRIOT.value: "Cypriot",
    NationalityId.CZECH.value: "Czech",
    NationalityId.DANISH.value: "Danish",
    NationalityId.DUTCH.value: "Dutch",
    NationalityId.ECUADORIAN.value: "Ecuadorian",
    NationalityId.ENGLISH.value: "English",
    NationalityId.EMIRIAN.value: "Emirian",
    NationalityId.ESTONIAN.value: "Estonian",
    NationalityId.FINNISH.value: "Finnish",
    NationalityId.FRENCH.value: "French",
    NationalityId.GERMAN.value: "German",
    NationalityId.GHANAIAN.value: "Ghanaian",
    NationalityId.GREEK.value: "Greek",
    NationalityId.GUATEMALAN.value: "Guatemalan",
    NationalityId.HONDURAN.value: "Honduran",
    NationalityId.HONG_KONGER.value: "Hong Konger",
    NationalityId.HUNGARIAN.value: "Hungarian",
    NationalityId.ICELANDER.value: "Icelander",
    NationalityId.INDIAN.value: "Indian",
    NationalityId.INDONESIAN.value: "Indonesian",
    NationalityId.IRISH.value: "Irish",
    NationalityId.ISRAELI.value: "Israeli",
    NationalityId.ITALIAN.value: "Italian",
    NationalityId.JAMAICAN.value: "Jamaican",
    NationalityId.JAPANESE.value: "Japanese",
    NationalityId.JORDANIAN.value: "Jordanian",
    NationalityId.KUWAITI.value: "Kuwaiti",
    NationalityId.LATVIAN.value: "Latvian",
    NationalityId.LEBANESE.value: "Lebanese",
    NationalityId.LITHUANIAN.value: "Lithuanian",
    NationalityId.LUXEMBOURGER.value: "Luxembourger",
    NationalityId.MALAYSIAN.value: "Malaysian",
    NationalityId.MALTESE.value: "Maltese",
    NationalityId.MEXICAN.value: "Mexican",
    NationalityId.MONEGASQUE.value: "Monegasque",
    NationalityId.NEW_ZEALANDER.value: "New Zealander",
    NationalityId.NICARAGUAN.value: "Nicaraguan",
    NationalityId.NORTHERN_IRISH.value: "Northern Irish",
    NationalityId.NORWEGIAN.value: "Norwegian",
    NationalityId.OMANI.value: "Omani",
    NationalityId.PAKISTANI.value: "Pakistani",
    NationalityId.PANAMANIAN.value: "Panamanian",
    NationalityId.PARAGUAYAN.value: "Paraguayan",
    NationalityId.PERUVIAN.value: "Peruvian",
    NationalityId.POLISH.value: "Polish",
    NationalityId.PORTUGUESE.value: "Portuguese",
    NationalityId.QATARI.value: "Qatari",
    NationalityId.ROMANIAN.value: "Romanian",
    NationalityId.RUSSIAN.value: "Russian",
    NationalityId.SALVADORAN.value: "Salvadoran",
    NationalityId.SAUDI.value: "Saudi",
    NationalityId.SCOTTISH.value: "Scottish",
    NationalityId.SERBIAN.value: "Serbian",
    NationalityId.SINGAPOREAN.value: "Singaporean",
    NationalityId.SLOVAKIAN.value: "Slovakian",
    NationalityId.SLOVENIAN.value: "Slovenian",
    NationalityId.SOUTH_KOREAN.value: "South Korean",
    NationalityId.SOUTH_AFRICAN.value: "South African",
    NationalityId.SPANISH.value: "Spanish",
    NationalityId.SWEDISH.value: "Swedish",
    NationalityId.SWISS.value: "Swiss",
    NationalityId.THAI.value: "Thai",
    NationalityId.TURKISH.value: "Turkish",
    NationalityId.URUGUAYAN.value: "Uruguayan",
    NationalityId.UKRAINIAN.value: "Ukrainian",
    NationalityId.VENEZUELAN.value: "Venezuelan",
    NationalityId.BARBADIAN.value: "Barbadian",
    NationalityId.WELSH.value: "Welsh",
    NationalityId.VIETNAMESE.value: "Vietnamese",
}