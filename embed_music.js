#!/usr/bin/env node
const fs = require('fs');

const RACE_MP3 = fs.readFileSync('/home/aipi/.openclaw/workspace/games/race_song.mp3');
const PARK_MP3 = fs.readFileSync('/home/aipi/.openclaw/workspace/games/park_song.mp3');

const raceB64 = RACE_MP3.toString('base64');
const parkB64 = PARK_MP3.toString('base64');

const raceUri = 'data:audio/mp3;base64,' + raceB64;
const parkUri = 'data:audio/mp3;base64,' + parkB64;

const musicBlock = `const RACE_MUSIC = '${raceUri}';
const PARK_MUSIC = '${parkUri}';
let M = (() => {
  let el = null, muted = false;
  function play(track) {
    if (muted) { if (el) { el.pause(); el = null; } return; }
    if (el) { el.pause(); el = null; }
    el = new Audio(track === 'race' ? RACE_MUSIC : PARK_MUSIC);
    el.loop = true; el.volume = 0.45;
    el.play().catch(() => {});
  }
  function stop() { if (el) { el.pause(); el = null; } }
  return { start: play, stop, toggle: () => { muted = !muted; if (muted) stop(); return muted; }, isMuted: () => muted };
})();
`;

fs.writeFileSync('/home/aipi/.openclaw/workspace/games/music_embed.js', musicBlock);

console.log('Race b64 length:', raceB64.length);
console.log('Park b64 length:', parkB64.length);
console.log('Music block written, size:', musicBlock.length, 'chars');