import { DatabaseSync } from 'node:sqlite';
import fs from 'node:fs';
export function localDatabase(file = ':memory:') {
  const db = new DatabaseSync(file); db.exec(fs.readFileSync(new URL('./schema.sql', import.meta.url),'utf8').replaceAll('--> statement-breakpoint',''));
  return { close: () => db.close(), prepare(sql) { return { bind(...args) { return { async first() { return db.prepare(sql).get(...args) ?? null; }, async run() { const result = db.prepare(sql).run(...args); return { meta: { changes: Number(result.changes) } }; } }; } }; } };
}
