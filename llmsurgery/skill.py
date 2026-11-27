r"""Read and work with Claude Code, Codex, and Antigravity session transcripts.

notation: /why

- read, search: dialog views, read-only functions by default; change: record-level tools; dialogs: `doc(aidialog.dlgskill)` first

### Every conversation: the mirror

- ipynb copy of every Claude session, Codex thread, and Antigravity conversation on this machine, synced automatically    /earlier discussions, decisions, work lost to compaction

```python
from llmsurgery.mirror import index
nbrg(pat, index().root)
```

- `index()` syncs first; shell: `sess-index`; `sess-index --force` rebuilds every notebook, after conversion code changes
- hit = dialog notebook: pass its path as `dlg` to dlgskill file functions, e.g. `summary_dlg(path)`, `find_msgs(pat, path)`, `view_msg(id, path)`
- `doc(llmsurgery.mirror)`: metadata keeping hits citable across reindexes; why the mirror doubles as an archive

### One session

- `d = sess_dlg(ref)`: Claude session, Codex thread, or Antigravity conversation (ID or unique prefix) → in-memory dialog, in a few seconds; each user turn → prompt message, its reply → that message's output
- read: `d.find_msgs(pat)`; `d.msg(id).view()`; `d.view(ids=...)`; `len(d.messages)` before `d.summary()`    /long session: thousands of messages
- dlgskill file functions need an ipynb path: shell command `sess2nb` saves the session as one
- `doc(llmsurgery.sess)`: finding a session on any host; what `sess_dlg` drops; when per-host `sess2dlg`, `thread2dlg`, or `conv2dlg` fits better

### Changing transcripts

| |Claude Code|Codex|Antigravity
-|-|-|-
load|`load_sess`|`load_recs`|`load_conv`
search|`sess_search`|`item_search`|`step_search`
read slice|`show_recs`|`show_items`|`show_steps`

- search hits carry the full record, item, or step; before changing: read module and function docs, inspect target records

### Other modules

- `ant`, `oai`, `agy`: where each host stores transcripts, finding/searching, and which operations write files
- `doc(aihist.hist)`: dialogs ↔ chat histories, replies
"""

__all__ = []
