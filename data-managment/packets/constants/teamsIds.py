from enum import Enum
from typing import Dict

class TeamId(Enum):
    MERCEDES = 0
    FERRARI = 1
    RED_BULL_RACING = 2
    WILLIAMS = 3
    ASTON_MARTIN = 4
    ALPINE = 5
    ALPHA_TAURI = 6
    HAAS = 7
    MCLAREN = 8
    ALFA_ROMEO = 9
    MERCEDES_2020 = 85
    FERRARI_2020 = 86
    RED_BULL_2020 = 87
    WILLIAMS_2020 = 88
    RACING_POINT_2020 = 89
    RENAULT_2020 = 90
    ALPHA_TAURI_2020 = 91
    HAAS_2020 = 92
    MCLAREN_2020 = 93
    ALFA_ROMEO_2020 = 94
    ASTON_MARTIN_DB11_V12 = 95
    ASTON_MARTIN_VANTAGE_F1_EDITION = 96
    ASTON_MARTIN_VANTAGE_SAFETY_CAR = 97
    FERRARI_F8_TRIBUTO = 98
    FERRARI_ROMA = 99
    MCLAREN_720S = 100
    MCLAREN_ARTURA = 101
    MERCEDES_AMG_GT_BLACK_SERIES_SAFETY_CAR = 102
    MERCEDES_AMG_GTR_PRO = 103
    F1_CUSTOM_TEAM = 104
    PREMA_21 = 106
    UNI_VIRTUOSI_21 = 107
    CARLIN_21 = 108
    HITECH_21 = 109
    ART_GP_21 = 110
    MP_MOTORSPORT_21 = 111
    CHAROUZ_21 = 112
    DAMS_21 = 113
    CAMPOS_21 = 114
    BWT_21 = 115
    TRIDENT_21 = 116
    MERCEDES_AMG_GT_BLACK_SERIES = 117
    PREMA_22 = 118
    VIRTUOSI_22 = 119
    CARLIN_22 = 120
    HITECH_22 = 121
    ART_GP_22 = 122
    MP_MOTORSPORT_22 = 123
    CHAROUZ_22 = 124
    DAMS_22 = 125
    CAMPOS_22 = 126
    VAN_AMERSFOORT_RACING_22 = 127
    TRIDENT_22 = 128

TEAMS_NAMES: Dict[int, str] = {
    TeamId.MERCEDES.value: "Mercedes",
    TeamId.FERRARI.value: "Ferrari",
    TeamId.RED_BULL_RACING.value: "Red Bull Racing",
    TeamId.WILLIAMS.value: "Williams",
    TeamId.ASTON_MARTIN.value: "Aston Martin",
    TeamId.ALPINE.value: "Alpine",
    TeamId.ALPHA_TAURI.value: "Alpha Tauri",
    TeamId.HAAS.value: "Haas",
    TeamId.MCLAREN.value: "McLaren",
    TeamId.ALFA_ROMEO.value: "Alfa Romeo",
    TeamId.MERCEDES_2020.value: "Mercedes 2020",
    TeamId.FERRARI_2020.value: "Ferrari 2020",
    TeamId.RED_BULL_2020.value: "Red Bull 2020",
    TeamId.WILLIAMS_2020.value: "Williams 2020",
    TeamId.RACING_POINT_2020.value: "Racing Point 2020",
    TeamId.RENAULT_2020.value: "Renault 2020",
    TeamId.ALPHA_TAURI_2020.value: "Alpha Tauri 2020",
    TeamId.HAAS_2020.value: "Haas 2020",
    TeamId.MCLAREN_2020.value: "McLaren 2020",
    TeamId.ALFA_ROMEO_2020.value: "Alfa Romeo 2020",
    TeamId.ASTON_MARTIN_DB11_V12.value: "Aston Martin DB11 V12",
    TeamId.ASTON_MARTIN_VANTAGE_F1_EDITION.value: "Aston Martin Vantage F1 Edition",
    TeamId.ASTON_MARTIN_VANTAGE_SAFETY_CAR.value: "Aston Martin Vantage Safety Car",
    TeamId.FERRARI_F8_TRIBUTO.value: "Ferrari F8 Tributo",
    TeamId.FERRARI_ROMA.value: "Ferrari Roma",
    TeamId.MCLAREN_720S.value: "McLaren 720S",
    TeamId.MCLAREN_ARTURA.value: "McLaren Artura",
    TeamId.MERCEDES_AMG_GT_BLACK_SERIES_SAFETY_CAR.value: "Mercedes AMG GT Black Series Safety Car",
    TeamId.MERCEDES_AMG_GTR_PRO.value: "Mercedes AMG GTR Pro",
    TeamId.F1_CUSTOM_TEAM.value: "F1 Custom Team",
    TeamId.PREMA_21.value: "Prema 21",
    TeamId.UNI_VIRTUOSI_21.value: "Uni Virtuosi 21",
    TeamId.CARLIN_21.value: "Carlin 21",
    TeamId.HITECH_21.value: "Hitech 21",
    TeamId.ART_GP_21.value: "ART GP 21",
    TeamId.MP_MOTORSPORT_21.value: "MP Motorsport 21",
    TeamId.CHAROUZ_21.value: "Charouz 21",
    TeamId.DAMS_21.value: "DAMS 21",
    TeamId.CAMPOS_21.value: "Campos 21",
    TeamId.BWT_21.value: "BWT 21",
    TeamId.TRIDENT_21.value: "Trident 21",
    TeamId.MERCEDES_AMG_GT_BLACK_SERIES.value: "Mercedes AMG GT Black Series",
    TeamId.PREMA_22.value: "Prema 22",
    TeamId.VIRTUOSI_22.value: "Virtuosi 22",
    TeamId.CARLIN_22.value: "Carlin 22",
    TeamId.HITECH_22.value: "Hitech 22",
    TeamId.ART_GP_22.value: "ART GP 22",
    TeamId.MP_MOTORSPORT_22.value: "MP Motorsport 22",
    TeamId.CHAROUZ_22.value: "Charouz 22",
    TeamId.DAMS_22.value: "DAMS 22",
    TeamId.CAMPOS_22.value: "Campos 22",
    TeamId.VAN_AMERSFOORT_RACING_22.value: "Van Amersfoort Racing 22",
    TeamId.TRIDENT_22.value: "Trident 22",
}