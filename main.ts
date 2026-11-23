// news-image-20261123 entry program (Node 22, standard library only).
//
// The entry image is drawn by draw.py and stored beside this file as
// entry.png. This program walks the file as a PNG document — signature,
// every chunk with its CRC32, the IHDR dimensions, and a terminating IEND
// exactly at end of file — and only then copies it to the output directory.
// The copy is byte-for-byte, so repeated runs write identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;
const SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

// CRC-32 (IEEE 802.3) table, built once at startup.
const CRC_TABLE: Uint32Array = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(bytes: Buffer, start: number, end: number): number {
  let crc = 0xffffffff;
  for (let i = start; i < end; i++) {
    crc = CRC_TABLE[(crc ^ bytes[i]) & 0xff] ^ (crc >>> 8);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function fail(message: string): never {
  throw new Error(`entry.png rejected: ${message}`);
}

function main(): void {
  const root = dirname(resolve(process.argv[1]));
  const source = join(root, "entry.png");
  const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
  const target = join(outDir, "entry.png");

  const bytes = readFileSync(source);
  if (bytes.length > MAX_BYTES) {
    fail(`size ${bytes.length} bytes exceeds the ${MAX_BYTES} byte limit`);
  }
  if (bytes.length < 8) {
    fail("file is too short to be a PNG");
  }
  for (let i = 0; i < SIGNATURE.length; i++) {
    if (bytes[i] !== SIGNATURE[i]) {
      fail("first bytes are not the PNG signature");
    }
  }

  // Walk the chunks: length (4) + type (4) + data + CRC (4), verifying
  // each stored CRC against the CRC of type+data, and noting the IHDR.
  let offset = 8;
  let width = 0;
  let height = 0;
  let sawIend = false;
  let sawIdat = false;
  while (offset + 12 <= bytes.length) {
    const length = bytes.readUInt32BE(offset);
    const type = bytes.toString("ascii", offset + 4, offset + 8);
    if (offset + 12 + length > bytes.length) {
      fail(`chunk ${type} at offset ${offset} runs past end of file`);
    }
    const stored = bytes.readUInt32BE(offset + 8 + length);
    const computed = crc32(bytes, offset + 4, offset + 8 + length);
    if (stored !== computed) {
      fail(`chunk ${type} has a bad CRC (stored ${stored}, computed ${computed})`);
    }
    if (type === "IHDR") {
      if (length !== 13) fail("IHDR is not 13 bytes");
      width = bytes.readUInt32BE(offset + 8);
      height = bytes.readUInt32BE(offset + 12);
    }
    if (type === "IDAT") sawIdat = true;
    offset += 12 + length;
    if (type === "IEND") {
      sawIend = true;
      break;
    }
  }
  if (!sawIend) fail("no terminating IEND chunk");
  if (offset !== bytes.length) {
    fail(`trailing ${bytes.length - offset} bytes after IEND`);
  }
  if (!sawIdat) fail("no IDAT image data chunk");
  if (width === 0 || height === 0) fail("missing IHDR dimensions");
  if (width > MAX_SIDE || height > MAX_SIDE) {
    fail(`dimensions ${width}x${height} exceed ${MAX_SIDE}x${MAX_SIDE}`);
  }

  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, target);
  console.log(`entry.png OK: ${width}x${height}, ${bytes.length} bytes -> ${target}`);
}

main();
