"""Read and work with Claude Code and Codex session transcripts.

Use the mirror to find earlier discussions, decisions, or work lost to compaction. It stores ipynb copies of every Claude session and Codex thread on this machine, kept in sync automatically.

```python
from llmsurgery.mirror import index
nbrg(pat, index().root)
```

This searches every conversation you have ever had with either agent. `index()` syncs before returning. It uses a stat-only pass when nothing changed and an incremental rebuild otherwise. The search is always current. Use `sess-index` from the CLI, with `--force` after conversion changes.

Hits are ordinary dialogs. Read them with `find_msgs`, `summary_dlg`, and `view_msg`. Notebook metadata records the source transcript and the conversation's true time span. Message metadata retains each source record's `created` time and `uid`. Message IDs are deterministic. Hits stay citable across reindexes. Mirrors of garbage-collected transcripts are kept: the mirror doubles as an archive.

Use `sess_dlg(ref)` to read one session. It accepts a session ID or unique prefix from either Claude Code or Codex and returns the conversation with bookkeeping and injected turns dropped. `sess2dlg` (Claude Code) and `thread2dlg` (Codex) are the faithful per-host conversions. All cost a fraction
of a second and turn tens of thousands of records into a summary of a few dozen
rows.

Use `d.summary()` to inspect message sizes before deciding what to read. Search with `d.find_msgs(pat)` and read messages with `view_msg` or `view_msgs`. `doc(aidialog.dlgskill)` explains these tools. The `sess2nb` command writes the conversation to an ipynb at a path you choose.

Use record-level tools to change transcripts. For reading conversations, use the dialog tools above.

- Load records with `load_sess` or `load_recs`.
- Search with `sess_search` or `item_search`. Each hit contains its full record on `.rec` or its full item on `.item`. You do not need to calculate an index to read it.
- Read a slice with `show_recs` or `show_items`.

Use `doc(llmsurgery.ant)` for Claude Code JSONL sessions and prompt history.
Use `doc(llmsurgery.oai)` for Codex rollout files. Those module docs explain
where transcripts live, how to locate and search them, and which operations
write files.
Use `doc(llmsurgery.sess)` for finding a session on either host and reading it.
Use `doc(llmsurgery.mirror)` for the mirror and its indexing.

Use `doc(aidialog.hist)` for conversions between dialogs and chat histories or
replies. Use `doc(llmsurgery.compact)` for compact conversation documents and
transcript compaction.

Inspect sessions through the read-only functions by default. Before changing a
transcript, read the relevant module and function docs and inspect the target
records.
"""

__all__ = []
