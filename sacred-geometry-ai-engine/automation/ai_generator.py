import datetime
import random
from pathlib import Path

TOPICS = [
    "Golden Ratio Architecture",
    "Fibonacci Structural Design",
    "Sacred Geometry Homes",
    "Energy Efficient Buildings",
    "Spiritual Alignment Spaces",
]

CONCEPTS = [
    "Solar-aligned courtyard residence",
    "Modular phi-ratio co-living pod",
    "Spiral circulation wellness retreat",
    "Passive-cooling harmonic dome",
    "Community temple with fractal zoning",
]


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def generate_book_content() -> str:
    topic = random.choice(TOPICS)
    return f"""
\n## Chapter Update ({utc_now()})

**Topic:** {topic}

### Concept
Sacred geometry applied to architecture creates coherent and efficient environments aligned with proportion principles.

### Application
- Structural efficiency
- Energy flow optimization
- Durable, modular planning

### Monetization
Convert this section into:
- Book chapter expansion
- Course lesson module
- Blueprint/package offer
"""


def generate_architecture_concept() -> str:
    concept = random.choice(CONCEPTS)
    return f"""
\n## New Geometry Design ({utc_now()})

**Design Concept:** {concept}

### Features
- Ratio emphasis: 1 : 1.618
- Natural ventilation pathways
- Solar orientation strategy

### Material Direction
- Reinforced concrete
- Steel framing
- High-performance glazing

### Profit Potential
Package as premium concept design + consulting add-on.
"""


def update_files() -> None:
    root = Path(__file__).resolve().parent.parent
    manuscript = root / "book/manuscript.md"
    geometry = root / "geometry/geometry_diagrams.md"

    with manuscript.open("a", encoding="utf-8") as handle:
        handle.write(generate_book_content())

    with geometry.open("a", encoding="utf-8") as handle:
        handle.write(generate_architecture_concept())


if __name__ == "__main__":
    update_files()
