/**
 * Builds assets/city-index.txt - the offline "is this a real city?" dictionary
 * used to gate WeatherAPI calls.
 *
 * Source: GeoNames cities15000 (every city on earth with population >= 15,000),
 * licensed CC BY 4.0 - https://download.geonames.org/export/dump/
 *
 * Usage:  node tools/build-city-index.mjs <path-to-cities15000.txt>
 *
 * Output: one normalised city name per line, sorted and de-duplicated.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const SOURCE = process.argv[2];
const OUT = resolve(process.argv[3] || 'assets/city-index.txt');

if (!SOURCE) {
  console.error('usage: node tools/build-city-index.mjs <cities15000.txt> [out]');
  process.exit(1);
}

/** Lower-case, strip accents, collapse whitespace. Must match CityIndexService. */
function normalise(value) {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
}

// Keep Latin-script alternate names (English exonyms such as Munich, Cologne,
// Florence) and drop the CJK / Cyrillic / Arabic ones, which no one will type
// into this input and which would triple the file size.
const LATIN_ONLY = /^[\x20-\x7E\u00C0-\u024F'.-]+$/;

const names = new Set();
let cities = 0;

for (const line of readFileSync(SOURCE, 'utf8').split('\n')) {
  if (!line.trim()) continue;
  const f = line.split('\t');
  const [, name, asciiname] = f;
  if (!name) continue;
  cities++;

  for (const candidate of [name, asciiname]) {
    if (!candidate) continue;
    if (!LATIN_ONLY.test(candidate)) continue;
    const n = normalise(candidate);
    // 2 chars is the shortest real city name (e.g. "Y"); 60 filters junk rows.
    if (n.length < 2 || n.length > 60) continue;
    names.add(n);
  }
}

const sorted = [...names].sort();
mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, sorted.join('\n') + '\n', 'utf8');

console.log(`cities read      : ${cities}`);
console.log(`unique names out : ${sorted.length}`);
console.log(`file             : ${OUT}`);
console.log(`bytes            : ${Buffer.byteLength(sorted.join('\n')).toLocaleString()}`);
