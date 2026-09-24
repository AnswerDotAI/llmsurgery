"""Read and work with Claude Code and Codex session transcripts.

Read and search conversations via dialog views; change transcripts via record-level tools. Inspect sessions with the read-only functions by default.

# Searching every conversation

The mirror keeps an ipynb copy of every Claude session and Codex thread on this machine, synced automatically. Use it to find earlier discussions, decisions, or work lost to compaction:

```python
from llmsurgery.mirror import index
nbrg(pat, index().root)
```

This covers every conversation you've had with either agent. `index()` syncs before returning, so search is always current; from the shell, `sess-index` does the same, and `--force` rebuilds everything after conversion changes. Hits are ordinary dialogs: read them with `find_msgs`, `summary_dlg`, `view_msg`. `doc(llmsurgery.mirror)` covers the metadata keeping hits citable across reindexes, and why the mirror doubles as an archive.

# Reading one session

`sess_dlg(ref)` opens a Claude session or Codex thread as a dialog, from its ID or a unique prefix; `doc(llmsurgery.sess)` covers what it drops and when to use the per-host `sess2dlg`/`thread2dlg` instead. These conversions take a fraction of a second, turning tens of thousands of records into a summary of a few dozen rows. Check message sizes with `d.summary()` before choosing what to read, then use `d.find_msgs(pat)`, `view_msg`, or `view_msgs` (see `doc(aidialog.dlgskill)`). The `sess2nb` command saves a session as a notebook.

# Changing transcripts

Load records with `load_sess` (Claude Code) or `load_recs` (Codex); search them with `sess_search`/`item_search`, whose hits carry the full record or item; read a slice with `show_recs`/`show_items`. Before changing a transcript, read the relevant module and function docs, and inspect the target records.

# Module guide

- `doc(llmsurgery.ant)`: Claude Code JSONL sessions and prompt history
- `doc(llmsurgery.oai)`: Codex rollout files
- `doc(llmsurgery.sess)`: finding a session on either host and reading it
- `doc(llmsurgery.mirror)`: the mirror and its indexing
- `doc(llmsurgery.compact)`: compact conversation documents and transcript compaction
- `doc(aidialog.hist)`: conversions between dialogs and chat histories or replies

The `ant` and `oai` docs cover where transcripts live, how to find and search them, and which operations write files.
"""

__all__ = []
