"""Read and work with Claude Code and Codex session transcripts.

To find something in a session -- an earlier discussion, a decision, work lost to
compaction -- convert it to a dialog first: `sess2dlg` (Claude Code) and
`thread2dlg` (Codex) cost a fraction of a second and turn tens of thousands of
records into a summary of a few dozen rows. `d.summary()` is then the map (each
row sized, so how much to read answers itself), `d.find_msgs(pat)` the search,
and `view_msg`/`view_msgs` the read; `doc(aidialog.dlgskill)` covers that layer.
A dialog saved with `write_ipynb` is an ordinary ipynb whose prompt sources carry
their replies, so `rgapi`'s `nbrg` searches whole sessions across files, replies
included, returning cell ids the message tools take and matched lines within each.

Work at the record level for surgery, not for reading: `load_sess`/`load_recs` to
load, `sess_search`/`item_search` to search (every hit carries its own record or
item on `.rec`/`.item`, so a hit needs no index arithmetic to read in full), and
`show_recs`/`show_items` to read a slice.

Use `doc(llmsurgery.ant)` for Claude Code JSONL sessions and prompt history.
Use `doc(llmsurgery.oai)` for Codex rollout files. Those module docs explain
where transcripts live, how to locate and search them, and which operations
write files.

Use `doc(llmsurgery.hist)` for conversions between aidialog dialogs and
fastllm chat histories or replies. Use `doc(llmsurgery.compact)` for compact
conversation documents and transcript compaction.

Inspect sessions through the read-only functions by default. Before changing a
transcript, read the relevant module and function docs and inspect the target
records.
"""

__all__ = []
