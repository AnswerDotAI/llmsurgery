# NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.
"""Read and work with Claude Code and Codex session transcripts.

notation: /why

- read, search: dialog views, read-only functions by default; change: record-level tools; dialogs: `doc(aidialog.dlgskill)` first

# Every conversation: the mirror

- ipynb copy of every Claude session and Codex thread on this machine, synced automatically    /earlier discussions, decisions, work lost to compaction

```python
from llmsurgery.mirror import index
nbrg(pat, index().root)
```

- `index()` syncs first; shell: `sess-index`; `sess-index --force` rebuilds every notebook, after conversion code changes
- hit = dialog notebook: pass its path as `dlg` to dlgskill file functions, e.g. `summary_dlg(path)`, `find_msgs(pat, path)`, `view_msg(id, path)`
- `doc(llmsurgery.mirror)`: metadata keeping hits citable across reindexes; why the mirror doubles as an archive

# One session

- `d = sess_dlg(ref)`: Claude session or Codex thread (ID or unique prefix) → in-memory dialog, in a few seconds; each user turn → prompt message, its reply → that message's output
- read: `d.find_msgs(pat)`; `d.msg(id).view()`; `d.view(ids=...)`; `len(d.messages)` before `d.summary()`    /long session: thousands of messages
- dlgskill file functions need an ipynb path: shell command `sess2nb` saves the session as one
- `doc(llmsurgery.sess)`: finding a session on either host; what `sess_dlg` drops; when per-host `sess2dlg` or `thread2dlg` fits better

# Changing transcripts

| |Claude Code|Codex
-|-|-
load|`load_sess`|`load_recs`
search|`sess_search`|`item_search`
read slice|`show_recs`|`show_items`

- search hits carry the full record or item; before changing: read module and function docs, inspect target records

# Other modules

- `doc(llmsurgery.ant)`: Claude Code JSONL sessions, prompt history; `doc(llmsurgery.oai)`: Codex rollout files; both: where transcripts live, finding and searching them, which operations write files
- `doc(llmsurgery.compact)`: compact conversation documents, transcript compaction
- `doc(aihist.hist)`: dialogs ↔ chat histories, replies
"""

__all__ = []
