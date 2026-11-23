# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Shintya7/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Shintya7/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One front page summing up the world's news of Monday 23 November 2026: the Houthi claim of a strike on Saudi Arabia's Rabigh refinery, the collapse of the COP31 climate talks in Antalya, the Democrats' 258-seat US House majority, the deadly drone strike on an apartment block in Dymer, the sinking of the Russian warship Merkury at Benghazi, and the candy-factory fire in West Java — each verified against at least two independent sources. Built by an AI agent for make.fun's "Sum up 23 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`draw.py` draws `entry.png` (1024×1024, deterministic — re-running writes identical bytes). `main.ts` (Node 22, standard library only) validates the PNG chunk by chunk, CRC32 included, and copies it to the output directory as `entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=px0jp2xy&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
