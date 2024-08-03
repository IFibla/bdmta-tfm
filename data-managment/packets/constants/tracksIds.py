from enum import Enum
from typing import Dict

class TrackId(Enum):
    MELBOURNE = 0
    PAUL_RICARD = 1
    SHANGHAI = 2
    SAKHIR_BAHRAIN = 3
    CATALUNYA = 4
    MONACO = 5
    MONTREAL = 6
    SILVERSTONE = 7
    HOCKENHEIM = 8
    HUNGARORING = 9
    SPA = 10
    MONZA = 11
    SINGAPORE = 12
    SUZUKA = 13
    ABU_DHABI = 14
    TEXAS = 15
    BRAZIL = 16
    AUSTRIA = 17
    SOCHI = 18
    MEXICO = 19
    BAKU_AZERBAIJAN = 20
    SAKHIR_SHORT = 21
    SILVERSTONE_SHORT = 22
    TEXAS_SHORT = 23
    SUZUKA_SHORT = 24
    HANOI = 25
    ZANDVOORT = 26
    IMOLA = 27
    PORTIMÃO = 28
    JEDDAH = 29
    MIAMI = 30

TRACK_NAMES: Dict[int, str] = {
    TrackId.MELBOURNE.value: 'Albert Park Circuit',
    TrackId.PAUL_RICARD.value: 'Circuit Paul Ricard',
    TrackId.SHANGHAI.value: 'Shanghai International Circuit',
    TrackId.SAKHIR_BAHRAIN.value: 'Bahrain International Circuit',
    TrackId.CATALUNYA.value: 'Circuit de Barcelona-Catalunya',
    TrackId.MONACO.value: 'Circuit de Monte Carlo',
    TrackId.MONTREAL.value: 'Circuit Gilles-Villeneuve',
    TrackId.SILVERSTONE.value: 'Silverstone Circuit',
    TrackId.HOCKENHEIM.value: 'Hockenheimring',
    TrackId.HUNGARORING.value: 'Hungaroring',
    TrackId.SPA.value: 'Circuit Spa-Francorchamps',
    TrackId.MONZA.value: 'Autodromo Nazionale Monza',
    TrackId.SINGAPORE.value: 'Marina Bay Circuit',
    TrackId.SUZUKA.value: 'Suzuka Circuit',
    TrackId.ABU_DHABI.value: 'Yas Marina Circuit',
    TrackId.TEXAS.value: 'Circuit of the Americas',
    TrackId.BRAZIL.value: 'Autódromo José Carlos Pace',
    TrackId.AUSTRIA.value: 'Red Bull Ring',
    TrackId.SOCHI.value: 'Sochi Autodrom',
    TrackId.MEXICO.value: 'Autódromo Hermanos Rodríguez',
    TrackId.BAKU_AZERBAIJAN.value: 'Baku City Circuit',
    TrackId.SAKHIR_SHORT.value: 'Sakhir Short',
    TrackId.SILVERSTONE_SHORT.value: 'Silverstone Short',
    TrackId.TEXAS_SHORT.value: 'Texas Short',
    TrackId.SUZUKA_SHORT.value: 'Suzuka Short',
    TrackId.HANOI.value: 'Hanoi Circuit',
    TrackId.ZANDVOORT.value: 'Circuit Zandvoort',
    TrackId.IMOLA.value: 'Autodromo Enzo e Dino Ferrari',
    TrackId.PORTIMÃO.value: 'Algarve International Circuit',
    TrackId.JEDDAH.value: 'Jeddah Corniche Circuit',
    TrackId.MIAMI.value: 'Miami International Autodrome',
}
"""Associates a track id with that track's full name."""
