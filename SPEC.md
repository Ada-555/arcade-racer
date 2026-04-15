# ARCADE RACER — Your Gateway to Automotive Excellence

Welcome to **ARCADE RACER**, a curated collection of browser-based driving experiences built for every screen. Whether you're dodging traffic on a 6-lane highway or threading a car into a impossibly tight spot, this is your cockpit.

## Quick Start

Open `index.html` in any modern browser. Choose your game. Play.

## Games

### 🏁 Race Mode
Dodge traffic on a scrolling highway. Collect stars. Survive.
- **Controls:** Arrow keys or WASD to change lanes | SPACE to boost | P to pause
- **Objective:** Last as long as possible while collecting gold stars
- **Lives:** Start with 2, collect stars to earn more
- **Scoring:** Points accumulate over time

### 🅿️ Parking Sim
Top-down precision driving across 3 levels of increasing difficulty.
- **Controls:** Arrow keys or WASD (UP = forward | DOWN = reverse | LEFT/RIGHT = steer) | SPACE to confirm | P to pause
- **Objective:** Park the purple car in the green target zone
- **Lives:** 3 per game | Collisions cost a life
- **Scoring:** 1000 base minus time penalty + precision bonus for clean parking

## Platform Support

| Platform | Primary Controls | Notes |
|----------|-----------------|-------|
| PC | Keyboard (Arrow/WASD) | Full keyboard support |
| Mobile | Touch D-pad overlay | Responsive, touch-friendly |
| TV | Gamepad | D-pad + A button |

## Technical Notes

- Pure HTML5 Canvas — no external dependencies
- Web Audio API — all sounds synthesized, no audio files
- Single self-contained HTML file per game
- Automatic platform detection on load

## File Structure

```
games/
├── index.html       # All games + homepage (this repo)
├── SPEC.md          # This file
└── .learnings/      # Development notes
```

## Development Log

### 2026-04-15 — Initial Build
- Race Mode: 6-lane highway, lane-snap movement, enemy cars from both ends
- Parking Sim: Top-down physics, 3 levels, collision detection
- Platform detection: PC, Mobile, TV
- Web Audio synthesis: engine hum, star collect, crash, success chime
- Homepage: Dark blue (#1a1a2e) with game selector grid

## Lessons Learned

- Lane-snap movement (instant snap, no tween) feels more arcade-y than smooth transitions
- Enemy cars should spawn off-screen and scroll toward a center vanishing point for pseudo-3D effect
- Parking physics: forward/back velocity independent of steering angle, car rotates based on speed and steer input
- Collision detection: AABB for rectangular cars, rotated rect intersection for accurate top-down
- Web Audio: AudioContext must be resumed after user gesture (click/tap) to avoid silent first sounds
