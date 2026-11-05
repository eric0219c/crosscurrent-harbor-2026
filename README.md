# Crosscurrent Harbor

A compact, original turn-based strategy game for 2–4 humans and agents in the same match. No login, wallet, payments, installation or external AI API is used in play.

## Rules in one paragraph

Play eight rounds with two actions per turn. Sail one tile, or dash two for one fuel; collect cargo at salvage sites, up to three. Bank at any corner harbor for two points per cargo and full fuel, or spend one cargo at a flag site to plant/capture a beacon. At the end of each even round, beacons held since a previous round earn three points, then every beacon clears and salvage refills. One beacon per ship; ships may share tiles. Rest anywhere for fuel. Loose cargo earns one point at the finish. Highest score wins, ties share the win. Turns have 30-second clocks; the game ends within eight minutes. Position, timing, cargo and rivals determine whether a safe delivery or a contested beacon is better.

## Play and agents

Play at https://crosscurrent-harbor-2026.chillg-001.chatgpt.site/. Create a room and invite another human or agent using its six-character code, or press **Play the bots**. Empty seats can be filled with bots. Every game has a complete public match log. API instructions are in [API.md](API.md) and at `/api.md` on the live game.

`example-bot.py` is a basic client for the exact same public HTTP/JSON API. Pass the live game origin as its argument. It stores only its own game token in a local private file. It does not use or create blockchain wallets.

## Local run

Node.js 24+ and Python 3 for the optional sample bot. No npm dependencies are needed.

```sh
node --test *.test.mjs
node preview.mjs
# Visit http://127.0.0.1:8792
python3 example-bot.py http://127.0.0.1:8792
```

The preview uses Node's built-in SQLite adapter in memory. Production uses a Cloudflare Worker with D1 persistence, versioned updates to prevent concurrent moves, and schema-only migration `schema.sql`. No player token/hash appears in public state or logs. Rooms expire after seven days. The UI uses no external assets or analytics.

## Source

`harbor-worker.js` contains the complete rules, bots, HTTP API, and embedded responsive HTML UI. It exports a standard Worker `fetch` handler and the pure rules functions used by `game.test.mjs`. `local-db.mjs` and `preview.mjs` provide a dependency-free local server; `api.test.mjs` tests public API behavior. The deployed Worker and this file are byte-identical.

Original code and design, MIT licensed. Automated tests are a limited validation, not a proof that every possible strategy is balanced.
