"""Read and work with Claude Code and Codex session transcripts.

The likely main way to find something -- an earlier discussion, a decision, work
lost to compaction -- is the mirror: an ipynb copy of every Claude session and
Codex thread on the machine, kept in sync automatically. `from llmsurgery.mirror
import index` then `nbrg(pat, index().root)` searches every conversation you
have ever had with either agent: `index()` syncs before returning (a
stat-only pass when nothing changed, an incremental rebuild otherwise), so the
search is always current. Hits are ordinary dialogs -- `find_msgs`, `summary_dlg`,
`view_msg` read them -- with nb meta naming the source transcript and the
conversation's true time span, each message's meta carrying its source record's
`created` time and `uid`, and deterministic ids, so a hit stays citable across
reindexes. Mirrors of garbage-collected transcripts are kept: the mirror doubles
as an archive. `sess-index` is the CLI (`--force` after conversion changes).

To read one particular session, convert it directly: `sess_dlg(ref)` takes an id
from either host, as any unique prefix, and gives back the conversation with the
bookkeeping and injected turns dropped; `sess2dlg` (Claude Code) and
`thread2dlg` (Codex) are the faithful per-host conversions. All cost a fraction
of a second and turn tens of thousands of records into a summary of a few dozen
rows. `d.summary()` is then the map (each row sized, so how much to read answers
itself), `d.find_msgs(pat)` the search, and `view_msg`/`view_msgs` the read;
`doc(aidialog.dlgskill)` covers that layer. The `sess2nb` command writes the
same view to an ipynb wherever you choose.

Work at the record level for surgery, not for reading: `load_sess`/`load_recs` to
load, `sess_search`/`item_search` to search (every hit carries its own record or
item on `.rec`/`.item`, so a hit needs no index arithmetic to read in full), and
`show_recs`/`show_items` to read a slice.

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
