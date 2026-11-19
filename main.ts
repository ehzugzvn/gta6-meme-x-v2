// gta6-meme-x-01 entry v2 — "Download Day" (150 GB)
// Copies POST.json from the bot dir to the output dir for the grader.
// Node 22, standard library only. Deterministic, no network, no clock.
// The X post named by POST.json is the entry; this program only hands
// its address to the gate, byte for byte, after a light sanity check.
import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function isPostRecord(value: unknown): value is { url: string } {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof (value as { url?: unknown }).url === 'string' &&
    (value as { url: string }).url.trim().length > 0
  );
}

function main(): void {
  const source = join(BOT_DIR, 'POST.json');
  const target = join(OUTPUT_DIR, 'POST.json');

  let raw: string;
  try {
    raw = readFileSync(source, 'utf8');
  } catch (err) {
    fail(`cannot read POST.json from ${BOT_DIR}: ${(err as Error).message}`);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw!);
  } catch {
    fail('POST.json is not valid JSON');
  }

  if (!isPostRecord(parsed)) {
    fail('POST.json must be an object with a non-empty string "url"');
  }

  try {
    mkdirSync(OUTPUT_DIR, { recursive: true });
    copyFileSync(source, target);
  } catch (err) {
    fail(`cannot copy POST.json to ${OUTPUT_DIR}: ${(err as Error).message}`);
  }
}

main();
