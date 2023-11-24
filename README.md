# Snake-spel med Pygame

Det här repot innehåller ett Snake-spel byggt med Pygame-ramverket. Spelet är utformat med principer för objektorienterad programmering (OOP) och Entity-Component-System (ESC) designmönster.

## Funktioner

- Klassiskt Snake-spel med smidiga kontroller.
- Anpassningsbara inställningar genom `config.py`.
- Modulär design för enkel utvidgning och modifiering.

## Installation

Ingen installation krävs om du använder Replit-versionen av spelet. Besök följande länk för att spela direkt:
[Spela Snake på Replit](https://replit.com/teams/import/svoxniwhihbasupj-nti-tillmpat-programmering-2a)

För att köra spelet lokalt:

1. Klona repot:

```bash
git clone https://github.com/NTI-Tillampad-Programmering-2324/SnakeGame_ESC_with_Pygame
```

2. Installera Pygame:

```python
pip install pygame
```

## Användning

Kör `main.py` för att starta spelet:

## Struktur

- `components`: Spelkomponenter som riktning, position och rendering.
- `entities`: Definierar spelentiteter som ormen.
- `systems`: System som hanterar kollision, rörelse och rendering.

## Licens

Detta projekt är licensierat under MIT-licensen - se filen `LICENSE` för detaljer.

Utvecklat av KaahinAtNTI för kursen 'Tilllämpad Programmering' på NTI Gymnasiet Örebro, läsår 2023/24.
