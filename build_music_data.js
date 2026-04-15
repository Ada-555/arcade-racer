const fs = require('fs');
const path = require('path');

const raceFile = fs.readFileSync('/home/aipi/.openclaw/workspace/games/race_song.mp3');
const parkFile = fs.readFileSync('/home/aipi/.openclaw/workspace/games/park_song.mp3');

const raceB64 = raceFile.toString('base64');
const parkB64 = parkFile.toString('base64');

const raceDataUri = 'data:audio/mp3;base64,' + raceB64;
const parkDataUri = 'data:audio/mp3;base64,' + parkB64;

console.log('Race MP3 embedded, length:', raceB64.length);
console.log('Park MP3 embedded, length:', parkB64.length);
console.log('Race data URI prefix:', raceDataUri.substring(0, 50));
console.log('Park data URI prefix:', parkDataUri.substring(0, 50));

// Write as constants file for inclusion
const output = `// Auto-generated music data URIs
const RACE_MUSIC = '${raceDataUri}';
const PARK_MUSIC = '${parkDataUri}';
`;

fs.writeFileSync('/home/aipi/.openclaw/workspace/games/music_data.js', output);
console.log('music_data.js written');