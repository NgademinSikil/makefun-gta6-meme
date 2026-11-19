// "Me Looking at GTA 6" — entrypoint for make.fun's gta6-meme-x-01.
//
// This is the program the harness runs (Node 22, standard library only).
// Its one job is to hand the post to the grader: it copies POST.json from
// the repository root into $MAKEFUN_OUTPUT_DIR. The meme itself is drawn by
// main.py (Python, PIL) — see README.md — which the author ran beforehand
// to produce entry.png, the picture actually posted on X.
//
// Run it: mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const repoDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });

const postFile = join(repoDir, 'POST.json');
if (existsSync(postFile)) {
  copyFileSync(postFile, join(outDir, 'POST.json'));
  console.log('copied', join(outDir, 'POST.json'));
} else {
  console.error(
    'POST.json not in the repository yet: the post is made first, ' +
      'then POST.json is added before submitting.',
  );
}
