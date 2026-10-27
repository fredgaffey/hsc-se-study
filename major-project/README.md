# Major project: L Flip (Year 12 Software Engineering, AT3), full marks

My Year 12 major project: **L Flip**, a learner-driver logbook app with smart L-plate hardware. A learner starts a drive on their phone, the app logs hours and GPS, syncs to a server, and flips the physical L-plates over Bluetooth.

- **Stack:** HTML/CSS/JS (PWA + Capacitor native app), Python Flask, SQLite + SQLAlchemy, JWT auth, two ESP32 boards (GPS, accelerometer, Bluetooth, SD card).
- **Code:** the [`lflip/`](../lflip) submodule (github.com/fredgaffey/Lflip).
- **Result:** full marks.

These are the final documents, unedited. Earlier drafts and planning files are in [`archive/`](archive).

**[Logbook (final, complete).docx](Logbook%20(final,%20complete).docx)**: the whole logbook for both parts, including later entries (security hardening and more). The copies taken at each deadline are in `archive/logbook snapshots/`.

## Part 1: identifying, defining, research and planning

| File | What it is |
|---|---|
| [Part 1 - Documentation.pdf](part-1/Part%201%20-%20Documentation.pdf) | The documentation (easiest to read) |
| [Part 1 - Documentation.docx](part-1/Part%201%20-%20Documentation.docx) | Same document in Word |
| [Gantt chart.xlsx](part-1/Gantt%20chart.xlsx) | Project schedule |
| [diagrams/](part-1/diagrams) | Data flow diagram, storyboard, system and ESP32 server diagrams, trip design (PNG + the editable `.drawio`) |

## Part 2: producing, implementing, testing and evaluating

| File | What it is |
|---|---|
| [Part 2 - Documentation.docx](part-2/Part%202%20-%20Documentation.docx) | The Part 2 documentation |
| [Walkthrough video.mp4](part-2/Walkthrough%20video.mp4) | 15-minute walkthrough of the finished system (re-encoded from the submitted `.mov` to fit GitHub; same content) |
| [AI design.drawio](part-2/AI%20design.drawio) | Design of the AI feature |

The links inside the Part 2 documentation point to my school's SharePoint and only work for King's accounts. The files they point to (logbook and video) are the ones in this folder.

## Archive

Logbook snapshots from each deadline, planning documents, the project rubric, early pseudocode, a first Gantt chart, older diagram copies, the early drafts of the scaffolds, and a small Ollama chat experiment. Kept for reference. They are not the submitted versions.

## Tips if you're starting your own major project

- **Keep one master document** and export a PDF when you submit. I had version-history trouble at the end (several near-identical copies), so name the final one clearly and submit from one place.
- **Log as you go:** the logbooks are dated entries, not written at the end.
- **Draw the diagrams early** (DFD, storyboard, system diagram). They drive the design and they're marked.
