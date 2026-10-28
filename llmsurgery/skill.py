"""Read and work with Claude Code and Codex session transcripts.

Read and search conversations via dialog views; change transcripts via record-level tools. Inspect sessions with the read-only functions by default.

# Searching every conversation

The mirror keeps an ipynb copy of every Claude session and Codex thread on this machine, synced automatically. Use it to find earlier discussions, decisions, or work lost to compaction:

```python
from llmsurgery.mirror import index
nbrg(pat, index().root)
```

The mirror covers every conversation you've had with either agent. `index()` syncs it before returning. From the shell, `sess-index` does the same. After a change to the conversion code, `sess-index --force` rebuilds every notebook. `doc(llmsurgery.mirror)` covers the metadata that keeps hits citable across reindexes, and why the mirror doubles as an archive.

`aidialog` reads each mirror hit's notebook as a dialog. Read `doc(aidialog.dlgskill)` before reading one. Pass the notebook's path as `dlg` to `dlgskill`'s file functions, such as `summary_dlg(path)`, `find_msgs(pat, path)` and `view_msg(id, path)`.

# Reading one session

`sess_dlg(ref)` opens a Claude session or Codex thread, from its ID or a unique prefix, as an `aidialog` dialog held in memory. Read `doc(aidialog.dlgskill)` before reading one. Use the dialog's methods to read it. `dlgskill`'s file functions, such as `view_msg`, take only an ipynb path. Each user turn becomes a prompt message, with the reply as its output. A long session holds thousands of them. Converting one takes a few seconds. Check `len(d.messages)` before you call `d.summary()`. Search with `d.find_msgs(pat)`, then read one message with `d.msg(id).view()` or several with `d.view(ids=...)`. `doc(llmsurgery.sess)` covers what `sess_dlg` drops, and when to use the per-host `sess2dlg` or `thread2dlg` instead. To use the file functions, save the session as a notebook with the `sess2nb` command.

# Changing transcripts

Load records with `load_sess` (Claude Code) or `load_recs` (Codex); search them with `sess_search`/`item_search`, whose hits carry the full record or item; read a slice with `show_recs`/`show_items`. Before changing a transcript, read the relevant module and function docs, and inspect the target records.

# Module guide

- `doc(llmsurgery.ant)`: Claude Code JSONL sessions and prompt history
- `doc(llmsurgery.oai)`: Codex rollout files
- `doc(llmsurgery.sess)`: finding a session on either host and reading it
- `doc(llmsurgery.mirror)`: the mirror and its indexing
- `doc(llmsurgery.compact)`: compact conversation documents and transcript compaction
- `doc(aihist.hist)`: conversions between dialogs and chat histories or replies

The `ant` and `oai` docs cover where transcripts live, how to find and search them, and which operations write files.
"""

__all__ = []
