"""Find, read, and search Claude Code session transcripts and prompt history on this machine. Use this when a question concerns what happened in a Claude Code session: locating a conversation, reviewing or quoting what was said, or recovering work from a lost or rewritten transcript.

## Where sessions live

Claude Code stores each conversation as JSONL at `~/.claude/projects/<dir>/<session-id>.jsonl`, where `<dir>` is the project's absolute path with every non-alphanumeric character replaced by `-` (underscores included, and the path is resolved first, so on macOS a project in `/tmp/foo` files under `-private-tmp-foo`). `sess_dir` and `sess_file` compute these paths. A transcript is named by the conversation's first session id: `claude --resume` and post-compaction restarts advertise a fresh id in `CLAUDE_CODE_SESSION_ID` while appending records to the original file, so the env var can name an id with no file behind it. `cur_sess` resolves the live conversation another way, as the project's most recently modified transcript, and `resolve_session` accepts an id or a `/rename` title (`sess_by_name` looks titles up directly). Beside the `.jsonl`, a directory of the same name can hold oversized tool results (`tool-results/`) and subagent transcripts, and the project folder keeps a `memory/` dir.

## What a transcript holds

One JSON object per line. Six fields matter: `type`, `uuid`, `parentUuid`, `sessionId`, `timestamp`, and `message`, the last shaped like an Anthropic API message (`role` plus string-or-blocks `content`). Conversation records are `user` and `assistant`; a tool result is a `user` record carrying `tool_result` blocks, which `rec_role` reports as `tool`; everything else is bookkeeping. The active conversation is the `parentUuid` chain walked back from the last record (`sess_thread`); compaction starts a new chain, so `sess_thread` stops at the latest boundary while `load_sess` returns every record. `conv_recs` drops bookkeeping and `rec_txt` extracts a record's readable text.

Not every transcript records a live conversation: tooling writes synthetic sessions too (templates, forks, dialog conversions). Their records have deterministic v5 uuids (digit 13 is 5, where random ids have 4) and often share one timestamp.

## Prompt history

Separately from transcripts, every prompt typed on this machine is appended to `~/.claude/history.jsonl` with a millisecond timestamp and its project directory. `prompt_hist` reads it into filterable rows. When a transcript is lost or rewritten, the user's side of the conversation survives here.

## Workflow

Locate (`sess_file`, `cur_sess`, `resolve_session`), load (`load_sess`, or `load_recs` for any path), thread (`sess_thread`, `conv_recs`), search (`sess_search`, a regex over readable text returning match previews), read (`show_recs` for a slice, `sess2dlg` to browse a whole session as a dialog using the `aidialog.dlgskill` tools). Prefer `sess_search` over grepping the JSONL, which hits base64, signatures, and envelope noise.

Everything here is read-only. Writing, forking, and synthetic compaction live in `llmsurgery.ant` and `aidialog.compact`; read their docs before touching any transcript, since `save_sess` overwrites whole files.

Docs: https://AnswerDotAI.github.io/llmsurgery/ant.html.md
"""

__all__ = ['sess_dir', 'sess_file', 'cur_sess', 'resolve_session', 'sess_by_name', 'load_sess', 'load_recs',
           'sess_thread', 'conv_recs', 'rec_role', 'rec_txt', 'sess_search', 'show_recs', 'sess2dlg', 'prompt_hist']

from llmsurgery.ant import (sess_dir, sess_file, cur_sess, resolve_session, sess_by_name, load_sess, load_recs,
    sess_thread, conv_recs, rec_role, rec_txt, sess_search, show_recs, sess2dlg, prompt_hist)
