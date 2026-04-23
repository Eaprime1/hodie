# _TODAY/ — Daily Intake Layer
**The BBS inbox. Everything dials in here.**

## Purpose

_TODAY is the automated intake layer for HODIE. Content arrives here daily from:
- Email extracts
- Message threads  
- Device sync (Pixel 8a, Termux)
- Session exports from other repos
- Manual drops

The crawler processes this folder at least once daily, routes content to the
appropriate plexus stage, and moves processed files to `_TODAY/processed/`.

## Structure

```
_TODAY/
├── inbox/       ← Raw incoming content (drop zone)
├── processed/   ← Crawler-handled items (with timestamps)
└── daily/       ← Dated session summaries
```

## Chain of Custody

Every file entering `inbox/` gets:
1. Timestamp on arrival (filename prefix or metadata)
2. Source tag (where it came from)
3. Plexus assignment (crawler determines stage)
4. Move to processed/ with log entry

## Integration

This folder will absorb the `repo/today` content in Phase 3 of migration.
See `migrations/` for provenance logs.

**One intake per cycle. One hertz. BBS is always open.**
