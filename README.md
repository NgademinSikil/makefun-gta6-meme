# makefun-gta6-meme

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/NgademinSikil/makefun-gta6-meme/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/NgademinSikil/makefun-gta6-meme/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

"Me Looking at GTA 6" — a GTA 6 launch-week meme for make.fun's "Post a GTA 6 meme on X" bounty, in the classic distracted-boyfriend format: on a sunny Vice City street, "ME" turns around smitten to look at glamorous "GTA 6" (make.fun's white ghost in sunglasses and a gold chain, leaning under a pink neon "GTA 6" sign) while "MY RESPONSIBILITIES" stands behind him, arms crossed, glaring. The picture is drawn by `main.py` itself — original flat-cartoon figures with PIL, standard library plus Pillow, no fonts files of its own, no images, no network — so the meme is byte-for-byte reproducible. `main.ts` is the entrypoint the harness runs: it copies `POST.json` into the output directory (that is all it has to do). The meme was posted on X from a public account (see `POST.json` for the post); the caption is in `CAPTION.txt`.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out python3 main.py
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

The first command writes `out/entry.png` (the meme, 1024x1024); the second copies `out/POST.json` from the repository root when `POST.json` exists.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ds1567x3&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
