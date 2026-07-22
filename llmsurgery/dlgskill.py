"""Read, search, and edit dialogs and notebooks through the llmsurgery `Dialog`/`Message` model

Use this whenever the question or edit concerns a notebook's content: messages, sources, outputs, prompts and their replies.

## The hierarchy

Notebook work happens at three levels, and picking the right level is most of using this module well:

- Content (this module): what the messages say and how they change. `summary_dlg`, `find_msgs`, `view_dlg`, the message editing operations, and `reply2dlg`/`dlg2reply` for a prompt's reply.
- Representation (`fastcore.nbio`, formerly `execnb.nbio`): which keys exist, whether a file is schema-valid, whether bytes changed. Start with `validate_nb`/`validate_cell`, which name the offending cell; use `read_nb` directly when the question is about the dict itself. For *plain* notebooks (no dialog semantics), nbio's `Notebook`/`NbCell` objects and `cell_*` functions are the content surface, and this module's word choice marks the layer: cells for notebooks, messages for dialogs.
- Raw text: only when the file will not parse at all.

Dropping a level is correct exactly when the question is about the representation rather than the content ("why does Jupyter reject this file?", "did that write change any bytes?"). Treat each drop as a signal, though: needing nbio or raw JSON to answer a content question means a higher-level tool was missing. Re-read this module's docs to check it truly is missing, and then propose adding it rather than repeating the workaround.

## Core APIs

The function/method two-shapes contract is `fastcore.editskill`'s, learned once: the function is a transaction addressed by `dlg=` (an ipynb path, or None meaning the current dialog file: `set_dlg`); the method is a session on a held `Dialog` or `Message`, saved by an explicit `dlg.save()` (`msg_str_replace(id, ..., dlg=p)` ⟷ `m.str_replace(...)`). Wrapping any message list in an ephemeral `Dialog(msgs)` makes the whole session surface available on it.

- `summary_dlg(dlg)` / `d.summary()`: one preview line per message, `id:t:content` (t: c=code n=note p=prompt r=raw).
- `find_msgs(pattern, dlg, ...)`: search by regex, type, error state, heading, ids, or a `pred` (`symdef_finder`/`symref_finder`/`ast_finder` build structural ones); `context` defaults to 1 (the neighbouring message usually explains the match). Returns `MsgRow` snapshots (`id`, `msg_type`, `content`, `out`, `meta`), shown as preview lines. `d.find_msgs(...)` returns live `Message` objects in a `Msgs` list instead, edited directly rather than re-addressed. Every live message carries a `dlg` backref to its owning `Dialog`, so dialog-level operations are always in reach from a message in hand (e.g. `m.dlg.save()` after mutating `m.output` directly).
- `view_dlg(dlg)` / `d.view()` / `view_msg(id)` / `m.view()` / `view_msgs(*ids)` / `msg2xml(m)` / `m.to_xml()`: full views in the shared `item2xml` grammar (a prompt's reply is its `<out>` section); `incl_out=True` on the line views appends the message's output the same way.
- Structure: `add_msg`, `del_msgs`, `move_msgs`, `split_msg`, `merge_msgs`, `copy_msgs`/`cut_msgs`/`paste_msgs`, `create_dlg`, with session twins `d.move_msgs`, `m.split`, `d.merge_msgs`, `d.copy_msgs`/`d.cut_msgs`/`d.paste_msgs` (session adds go through `d.mk_message`, deletes through `d.remove_msgs`); the `%%add_msg` magic takes its body verbatim: its line is `%%add_msg [dlg] [msg_type] [before=|after=<id>]`, where a bare path token is the dlg and a bare type name the msg_type, and keyword spellings win over bare tokens.
- Text edits: `msg_str_replace`, `msg_strs_replace`, `msg_insert_line`, `msg_replace_lines`, `msg_del_lines`, `msg_ast_replace` (all with `re_filter`/line-range powers; `out=True` edits a prompt's reply or a code message's outputs literal), with the same names as `Message` methods for in-memory editing; `lnhashview_msg`/`msg_exhash` (and `m.lnhashview()`/`m.exhash()`) for hash-verified line edits (`lnhashview_msg` is `view_msg(..., lnhashs=True)`; only the exhash pair needs the `exhash` package).
- `reply2dlg(pmsg)`/`dlg2reply(sub)`: explode a reply into note/code messages and back; byte-exact for fmt2hist-clean replies.

## Idiomatic usage

Start by registering the notebook: `set_dlg(path)` makes every function here default to it (and clikernel's `%nbrun` magic follows suit), so calls read as "do this to message X". Then orient before acting:

- `summary_dlg()` first for anything sizable: a cheap one-line-per-message map. `view_dlg()` when you need the full story in order with ids. Read a notebook in full before describing or changing what it does - the interleaved prose, examples, and stored outputs (`incl_out=True`) are the design rationale.
- Read before probing: an ad-hoc "what happens if..." experiment usually re-derives, more slowly and less reliably, what an existing example cell already shows. If after reading you still need an experiment, that's a gap in the notebook - add it as a proper example cell so the next reader doesn't repeat it.
- `find_msgs` is the targeted view: keep the default `context=1` (the neighbouring markdown usually explains the match), and `ids=` with context is the positional query ("does A precede B?", "what's the idiom around here?"). Name questions are structural, not textual: `symdef_finder`/`symref_finder`/`ast_finder` beat regexes over binding syntax. Where available, rgapi's `nbrg` searches cell sources across files and returns the cell ids these functions take.
- Edit at the right level: `add_msg`/`%%add_msg` for new messages; within a message, prefer hash-verified addressing (`lnhashview_msg`/`msg_exhash`, or exhash's `lnhashview_cell`/`cell_exhash` by path and cell id) - view with the lnhash variant the moment an edit is plausible, so the view doubles as the edit's address book. The plain `msg_*` editors fit where exhash can't express the edit, e.g. one `msg_str_replace` across an id list. Never splice via `read_nb`/`write_nb` internals: if a primitive is missing here, stop and propose adding it.
- `dlg.validate()` catches model-level damage early; `dlg.save()` writes back. Don't wrap calls in defensive scaffolding (`hasattr`, `try/except`) - call directly and read the bare result.

Docs: https://AnswerDotAI.github.io/llmsurgery/dlgskill.html.md"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/05_dlgskill.ipynb.

# %% auto #0
__all__ = ['msg_insert_line', 'msg_str_replace', 'msg_strs_replace', 'msg_replace_lines', 'msg_del_lines', 'msg_ast_replace',
           'set_dlg', 'cur_dlg', 'summary_dlg', 'msg2xml', 'view_dlg', 'view_msg', 'view_msgs', 'find_msgs',
           'move_msgs', 'split_msg', 'merge_msgs', 'copy_msgs', 'cut_msgs', 'paste_msgs', 'symdef_finder',
           'symref_finder', 'ast_finder', 'lnhashview_msg', 'msg_exhash', 'add_msg', 'del_msgs', 'create_dlg',
           'add_msg_magic', 'load_ipython_extension', 'reply2dlg', 'dlg2reply']

# %% ../nbs/05_dlgskill.ipynb #a0aeb3fe
import shlex, re, copy
from fastcore.utils import *
from fastcore.meta import splice_sig, delegates
from fastcore.xtras import str_diff
from fastcore.xml import to_xml
from fastcore.nbio import item2xml
from fastcore.tools import insert_line, str_replace, strs_replace, replace_lines, del_lines, ast_replace, lnhash
from .dialog import *
from .ipynb import read_ipynb, write_ipynb
from .hist import reply2dlg, dlg2reply, render_outputs_ai  # chkstyle: ignore (re-exported via _all_)
_all_ = ['reply2dlg', 'dlg2reply']

# %% ../nbs/05_dlgskill.ipynb #278fa834
_cur_dlg = None

def set_dlg(
    fname, # ipynb path that later calls will default to
):
    "Set the current dialog file, used by these functions when `dlg` is None"
    global _cur_dlg
    _cur_dlg = Path(fname)
    return _cur_dlg

def cur_dlg():
    "A fresh `Dialog` read from the current dialog file (None if unset): the session-side entry to the ambient default"
    return read_ipynb(_cur_dlg) if _cur_dlg else None

def _to_dlg(x):
    "The dialog file `x` (None: the current dialog file), read fresh from disk"
    if isinstance(x, Dialog): raise TypeError('dlg= takes an ipynb path; on a live Dialog, call the method instead')
    if x is None: x = _cur_dlg
    if x is None: raise ValueError('No dialog: pass a path, or call set_dlg() first')
    return read_ipynb(x)

def _load_dlg(x):
    "`(dialog, True)`: read `x` from disk; the second element marks it ours to save"
    return _to_dlg(x), True

def _save(dlg, sv=True):
    "Write back to the file this call loaded from"
    if sv: dlg.save()

# %% ../nbs/05_dlgskill.ipynb #b120f853
@patch
def msg(self:Dialog,
    id, # A `Message` (matched by its id), or an id: exact, or unique prefix
):
    "The matching `Message` in this dialog"
    if isinstance(id, Message): id = id.id
    ms = [m for m in self.messages if m.id==id]
    if not ms: ms = [m for m in self.messages if m.id.startswith(id)]
    if len(ms) != 1: raise KeyError(f"{'ambiguous' if ms else 'no'} message id: {id!r}")
    return ms[0]

# %% ../nbs/05_dlgskill.ipynb #def6dd98
@patch
def summary(self:Dialog,
    maxlen:int=120, # Maximum characters per line
):
    "One `preview` line per message: `id:t:content` (t: c=code n=note p=prompt r=raw)"
    return self.messages.show(maxlen)

def summary_dlg(
    dlg=None, # An ipynb path; the current dialog file if None
    maxlen:int=120, # Maximum characters per line
):
    "One `preview` line per message of the dialog file"
    return _to_dlg(dlg).summary(maxlen)

# %% ../nbs/05_dlgskill.ipynb #9d26ea0f
_t2tag = dict(note='markdown')

def msg2xml(m, incl_out=False, trunc_out=True, ids=True):
    "One message as concise XML: content bare inside its type tag, with an `<out>` section for a code output or a prompt's reply"
    if m.msg_type==sprompt: o = m.ai_res
    elif incl_out and m.msg_type==scode and m.output:
        o = render_outputs_ai(m.output)
        if trunc_out: o = truncstr(o, 512)
    else: o = ''
    it = item2xml(_t2tag.get(m.msg_type, m.msg_type), m.content, o, id=m.id if ids else None,
                  kind=m.meta.get('rec_kind'), meta=m.meta)
    return to_xml(it, do_escape=False)

@patch
def to_xml(self:Message, incl_out=False, trunc_out=True, ids=True):
    "This message as concise XML (`msg2xml`)"
    return msg2xml(self, incl_out, trunc_out, ids)

@patch
def view(self:Dialog,
    incl_out:bool=False, # Include code outputs?
    only_errors:bool=False, # Show only code messages with error outputs (implies `incl_out`)?
    trunc_out:bool=True, # Truncate each output to ~512 chars?
):
    "This dialog as concise XML"
    ms = [m for m in self.messages if m.has_error] if only_errors else self.messages
    body = ''.join(msg2xml(m, incl_out or only_errors, trunc_out) for m in ms)
    return PrettyString(f'<dialog name="{self.name}">{body}</dialog>')

def view_dlg(
    dlg=None, # An ipynb path; the current dialog file if None
    incl_out:bool=False, # Include code outputs?
    only_errors:bool=False, # Show only code messages with error outputs (implies `incl_out`)?
    trunc_out:bool=True, # Truncate each output to ~512 chars?
):
    "The dialog file as concise XML"
    return _to_dlg(dlg).view(incl_out, only_errors, trunc_out)

# %% ../nbs/05_dlgskill.ipynb #04cc9cbd
@patch
def view(self:Message,
    nums:bool=True, # Show line numbers?
    start_line:int=1, # Starting line to view
    end_line:int=None, # End line (defaults to last line if None; -1 for EOF)
    lnhashs:bool=False, # Show exhash `lineno|hash|` addresses instead of line numbers?
    incl_out:bool=False, # Append the output (a prompt's reply, or code outputs) in an `<out>` block?
    trunc_out:bool=True, # Truncate an included output to ~512 chars?
):
    "This message's content with optional line numbers or exhash addresses"
    lines = self.content.splitlines()
    lines = lines[start_line-1:len(lines) if end_line in (None,-1) else end_line]
    res = '\n'.join((lnhash(i,l)+l if lnhashs else f'{i}: {l}' if nums else l) for i,l in enumerate(lines, start_line))
    if incl_out:
        o = self.ai_res if self.msg_type==sprompt else render_outputs_ai(self.output) if self.msg_type==scode and self.output else ''
        if o: res += f"\n<out>\n{truncstr(o, 512) if trunc_out else o}\n</out>"
    return PrettyString(res)

def view_msg(
    id, # Message id, looked up in `dlg` (unique prefixes allowed)
    dlg=None, # An ipynb path; the current dialog file if None
    nums:bool=True, # Show line numbers?
    start_line:int=1, # Starting line to view
    end_line:int=None, # End line (defaults to last line if None; -1 for EOF)
    lnhashs:bool=False, # Show exhash `lineno|hash|` addresses instead of line numbers?
    incl_out:bool=False, # Append the output (a prompt's reply, or code outputs) in an `<out>` block?
    trunc_out:bool=True, # Truncate an included output to ~512 chars?
):
    "Show a message's content with optional line numbers or exhash addresses"
    return _to_dlg(dlg).msg(id).view(nums, start_line, end_line, lnhashs, incl_out, trunc_out)

def view_msgs(
    *ids, # Message ids
    dlg=None, # An ipynb path; the current dialog file if None
    nums:bool=True, # Show line numbers?
    lnhashs:bool=False, # Show exhash `lineno|hash|` addresses instead of line numbers?
    incl_out:bool=False, # Append each output (a prompt's reply, or code outputs) in an `<out>` block?
    trunc_out:bool=True, # Truncate each included output to ~512 chars?
):
    "Show several messages, each preceded by a `# msg <id>` header"
    d = _to_dlg(dlg)
    return PrettyString('\n'.join(f"# msg {(m := d.msg(i)).id}\n{m.view(nums, lnhashs=lnhashs, incl_out=incl_out, trunc_out=trunc_out)}" for i in ids))

# %% ../nbs/05_dlgskill.ipynb #4bf78327
def _match_head(m, want):
    "Does `m` head the section `want` names? Exact first line when `want` starts with '#', hash-stripped text otherwise"
    if not m.header_level(): return False
    fl = m.content.split('\n', 1)[0]
    if want.startswith('#'): return fl.rstrip()==want.rstrip()
    return fl.lstrip('#').strip()==want.strip()

@patch
def find_msgs(self:Dialog,
    re_pattern:str='', # Regex over content (a prompt's reply included), DOTALL+MULTILINE; an invalid regex matches literally
    msg_type:str=None, # Optional limit by type ('code', 'note', 'prompt', or 'raw')
    only_err:bool=False, # Only code messages with error outputs?
    only_exp:bool=False, # Only exported messages (nbdev export directive in content or meta)?
    ids='', # Optionally filter by ids (comma-separated str, or list); results are always in dialog order, whatever order the ids are given
    before:int=0, # Also include n messages before each match
    after:int=0, # Also include n messages after each match
    context:int=None, # Messages of context around matches (default 1, or 0 when `headers_only`)
    limit:int=None, # Max matched messages
    use_case:bool=False, # Case-sensitive matching?
    use_regex:bool=True, # Regex matching (else plain substring)?
    headers_only:bool=False, # Only heading notes (an outline view)?
    header_section:str=None, # Return the section starting with this heading, plus its children
    pred:callable=None, # Extra match criterion, e.g. from `symdef_finder`/`symref_finder`/`ast_finder`, or host-specific flags
)->Msgs: # Live messages, so results can be edited directly
    "Find this dialog's messages matching all the given criteria"
    ms = self.messages
    if context is None: context = 0 if headers_only else 1
    if header_section is not None:
        head = first(m for m in ms if _match_head(m, header_section))
        ms = section_msgs(ms, head) if head else Msgs()
    if context: before = after = context
    flags = re.DOTALL|re.MULTILINE|(0 if use_case else re.IGNORECASE)
    if use_regex and re_pattern:
        try: re.compile(re_pattern)
        except re.error: use_regex = False
    pat = re.compile(re_pattern if use_regex else re.escape(re_pattern), flags) if re_pattern else None
    if isinstance(ids, str): ids = [o for o in ids.split(',') if o.strip()]
    idset = {self.msg(i.strip()).id for i in ids} if ids else None
    def _txt(m): return m.content + ('\n'+m.ai_res if m.msg_type==sprompt and m.ai_res else '')
    def _ok(m):
        if headers_only and not m.header_level(): return False
        if msg_type and m.msg_type!=msg_type: return False
        if only_err and not m.has_error: return False
        if only_exp and not m.exported: return False
        if pred and not pred(m): return False
        if idset is not None and m.id not in idset: return False
        return not pat or bool(pat.search(_txt(m)))
    hits = [i for i,m in enumerate(ms) if _ok(m)]
    if limit is not None: hits = hits[:limit]
    if before or after:
        keep = set()
        for i in hits: keep.update(range(max(0,i-before), min(len(ms), i+after+1)))
        hits = sorted(keep)
    return Msgs([ms[i] for i in hits])

@delegates(Dialog.find_msgs)
def find_msgs(
    re_pattern:str='', # Regex over content (a prompt's reply included), DOTALL+MULTILINE; an invalid regex matches literally
    dlg=None, # An ipynb path; the current dialog file if None
    **kwargs,
)->MsgRows: # Snapshot rows (`id`, `msg_type`, `content`, `out`, `meta`), shown as preview lines
    "Find messages in the dialog file matching all the given criteria; for live results, call `Dialog.find_msgs`"
    return MsgRows(MsgRow(m) for m in _to_dlg(dlg).find_msgs(re_pattern, **kwargs))

# %% ../nbs/05_dlgskill.ipynb #1afa6ffc
@patch
def move_msgs(self:Dialog,
    ids, # Message(s) or id(s) to move
    before=None, # Move before this message or id
    after=None, # Move after this message or id
):
    "Move messages, keeping their relative order; returns them"
    if (before is None) == (after is None): raise ValueError('Exactly one of before/after required')
    ms = Msgs([self.msg(i) for i in listify(ids)])
    self.remove_msgs(ms)
    idx = self.messages.index(self.msg(before if before is not None else after)) + (after is not None)
    self.messages[idx:idx] = ms
    return ms

def move_msgs(
    ids, # Message id(s) to move
    before=None, # Move before this message or id
    after=None, # Move after this message or id
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Move messages in the dialog file, keeping their relative order; returns them"
    d = _to_dlg(dlg)
    res = d.move_msgs(ids, before=before, after=after)
    _save(d)
    return res

# %% ../nbs/05_dlgskill.ipynb #4358a197
def _atts_for(content, att_map):
    "The attachments from `att_map` whose ids are referenced in `content`"
    return [a for aid,a in att_map.items() if aid in content]

@patch
def split(self:Message,
    *linenos:int, # Split before each of these 1-based lines
):
    "Split this message into pieces (returned as `Msgs`; the first keeps its id): one `'\\n\\n'` is absorbed at each cut (so `merge_msgs` restores blank-line-separated content byte-exactly), `meta_attrs` fields, the cell `meta`, and a leading `#| export` copy to every piece, attachments follow their references, and unreferenced ones stay on the first piece"
    d = self.dlg
    if d is None: raise ValueError('message is not in a dialog')
    lines = self.content.splitlines()
    cuts = [0, *[l-1 for l in linenos], len(lines)]
    parts = ['\n'.join(lines[a:b]) for a,b in zip(cuts, cuts[1:])]
    for i in range(len(parts)-1):  # each cut absorbs the '\n\n' that a later merge re-inserts
        if   parts[i].endswith('\n'):     parts[i] = parts[i][:-1]
        elif parts[i+1].startswith('\n'): parts[i+1] = parts[i+1][1:]
    src = self.content
    keep = {a: getattr(self, a) for a in self.meta_attrs if hasattr(self, a)}
    att_map = {a.id: a for a in self.attachments}
    refs = [_atts_for(p, att_map) for p in parts]
    used = {a.id for r in refs for a in r}
    refs[0] += [a for a in self.attachments if a.id not in used]
    self.content, self.attachments = parts[0], refs[0]
    prev, res = self, [self]
    for p,r in zip(parts[1:], refs[1:]):
        p = copy_export(p, src)
        prev = d.mk_message(p, after=prev, msg_type=self.msg_type, attachments=r, meta=copy.deepcopy(self.meta), **keep)
        res.append(prev)
    return Msgs(res)

def split_msg(
    id, # Message id to split
    *linenos:int, # Split before each of these 1-based lines
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Split a message in the dialog file (see `Message.split`)"
    d = _to_dlg(dlg)
    res = d.msg(id).split(*linenos)
    _save(d)
    return res

@patch
def merge_msgs(self:Dialog,
    *ids, # Adjacent messages or ids to merge
):
    "Merge into the first message (returned, keeping its id): same-type merges keep the type, mixed become a note via `merge_content`; metas and directives merge first-wins via `merge_parts`, outputs clear, attachments combine"
    ms = [self.msg(i) for i in ids]
    mtype = ms[0].msg_type if len(set(m.msg_type for m in ms))==1 else snote
    content, meta = merge_parts(ms, [m.merge_content(mtype) for m in ms])
    ms[0].update(content=content, meta=meta, output=None, msg_type=mtype, attachments=L(ms).attrgot('attachments').concat())
    self.remove_msgs(ms[1:])
    return ms[0]

def merge_msgs(
    *ids, # Adjacent message ids to merge
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Merge messages in the dialog file (see `Dialog.merge_msgs`)"
    d = _to_dlg(dlg)
    res = d.merge_msgs(*ids)
    _save(d)
    return res

# %% ../nbs/05_dlgskill.ipynb #928f2387
_paste_buf = []

@patch
def copy_msgs(self:Dialog,
    *ids, # Messages or ids to copy
):
    "Copy messages into the paste buffer (replacing its contents), for later `paste_msgs`"
    global _paste_buf
    _paste_buf = Msgs([self.msg(i) for i in ids])
    return _paste_buf

@patch
def cut_msgs(self:Dialog,
    *ids, # Messages or ids to cut
):
    "Copy messages into the paste buffer, then remove them from the dialog"
    res = self.copy_msgs(*ids)
    self.remove_msgs(res)
    return res

@patch
def paste_msgs(self:Dialog,
    before=None, # Insert before this message or id
    after=None, # Insert after this message or id
):
    "Insert copies of the buffered messages (fresh ids) before/after a message or id; returns the new messages"
    if before is not None: before = self.msg(before)
    if after is not None: after = self.msg(after)
    return Msgs(self.mk_messages(_paste_buf, before=before, after=after))

def copy_msgs(
    *ids, # Message ids to copy
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Copy messages into the paste buffer (replacing its contents), for later `paste_msgs`"
    return _to_dlg(dlg).copy_msgs(*ids)

def cut_msgs(
    *ids, # Message ids to cut
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Copy messages into the paste buffer, then remove them from the dialog file"
    d = _to_dlg(dlg)
    res = d.cut_msgs(*ids)
    _save(d)
    return res

def paste_msgs(
    before=None, # Insert before this message or id
    after=None, # Insert after this message or id
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Insert copies of the buffered messages (fresh ids) before/after a message or id in the dialog file; returns the new messages"
    d = _to_dlg(dlg)
    res = d.paste_msgs(before=before, after=after)
    _save(d)
    return res

# %% ../nbs/05_dlgskill.ipynb #9ef4dc1f
def _out_text(m):
    "A prompt's reply markdown, the only output editable as text"
    if m.msg_type != sprompt: raise ValueError(f"{m.id}: out=True edits a prompt's reply; assign `msg.output` directly for other types")
    return m.ai_res

def _set_out_text(m, s): m.output = s

# %% ../nbs/05_dlgskill.ipynb #3b31bc59
_msg_edit_doc = """
Be sure you've viewed the message (e.g. `view_msg`) so you know the line nums.

Message editing standard parameters:
- `id`: message id (or list of ids, or 'all'), unique prefixes allowed
- `dlg`: an ipynb path; the current dialog file if None
- `out`: edit the output text (prompt reply, or code outputs literal) instead of the source

returns: diff of changes, or "none: No changes.", or "error: ..."
"""

def _msg_edit(f, name=None):
    def wrapper(id, *args, dlg=None, out:bool=False, **kw):
        d, sv = _load_dlg(dlg)
        def _one(cid):
            m = d.msg(cid)
            try:
                text = _out_text(m) if out else m.content
                if not text: return f"error: Message has no {'output' if out else 'source'}"
                new = f(text, *args, **kw)
                if out: _set_out_text(m, new)
                else: m.content = new
            except Exception as e: return f'error: {e}'
            return str_diff(text, new) or 'none: No changes.'
        if isinstance(id, list) or id=='all':
            if id=='all': id = [m.id for m in d.messages]
            res = [(cid, r) for cid in id if not (r := _one(cid)).startswith('none:')]
        else: res = PrettyString(_one(id))
        _save(d, sv)
        return res
    res = splice_sig(wrapper, f, 'text')
    if name: res.__name__ = res.__qualname__ = name
    res.__doc__ = (f.__doc__ or '') + _msg_edit_doc
    return res

msg_insert_line   = _msg_edit(insert_line,   'msg_insert_line')
msg_str_replace   = _msg_edit(str_replace,   'msg_str_replace')
msg_strs_replace  = _msg_edit(strs_replace,  'msg_strs_replace')
msg_replace_lines = _msg_edit(replace_lines, 'msg_replace_lines')
msg_del_lines     = _msg_edit(del_lines,     'msg_del_lines')
msg_ast_replace   = _msg_edit(ast_replace,   'msg_ast_replace')

def _msg_method(f):
    def method(self, *args, out:bool=False, **kw):
        text = _out_text(self) if out else self.content
        if not text: return PrettyString(f"error: Message has no {'output' if out else 'source'}")
        try: new = f(text, *args, **kw)
        except ValueError as e: return PrettyString(f'error: {e}')
        if out: _set_out_text(self, new)
        else: self.content = new
        return PrettyString(str_diff(text, new) or 'none: No changes.')
    res = splice_sig(method, f, 'text')
    res.__name__ = res.__qualname__ = f.__name__
    res.__doc__ = (f.__doc__ or '') + "\nIn-memory edit of this message (`out=True` edits a prompt's reply), returning a diff; nothing is saved."
    return res

for _f in (insert_line, str_replace, strs_replace, replace_lines, del_lines, ast_replace): setattr(Message, _f.__name__, _msg_method(_f))

# %% ../nbs/05_dlgskill.ipynb #6f441ba4
__pyskill_params__ = {'replace_params': ('start_line', 'end_line', 'n_matches', 're_filter', 'invert_filter', 'use_regex')}

# %% ../nbs/05_dlgskill.ipynb #b3f84a46
def symdef_finder(name):
    "`find_msgs` predicate: does the message bind `name` at cell top level? (requires `remold`)"
    from remold import symdefs
    return lambda m: name in symdefs(m.content)

def symref_finder(name):
    "`find_msgs` predicate: does the message reference `name`? (requires `remold`)"
    from remold import symrefs
    return lambda m: name in symrefs(m.content)

def ast_finder(pattern):
    "`find_msgs` predicate: does ast-grep `pattern` match in the message? (requires `remold`)"
    from remold import astfind
    return lambda m: bool(astfind(m.content, pattern))

# %% ../nbs/05_dlgskill.ipynb #b6f8b9b3
@patch
def lnhashview(self:Message):
    "Hash-addressed view of this message's content, for `Message.exhash`"
    return self.view(lnhashs=True)

@patch
def exhash(self:Message,
    *cmds:tuple, # exhash command tuples, addresses from `lnhashview`
    sw:int=4, # Shift width for indent commands
):
    "Apply exhash commands to this message's content in memory, returning the diff"
    from exhash import exhash as _exhash
    res = _exhash(self.content, list(cmds), sw=sw)
    self.content = '\n'.join(res.lines)
    return PrettyString(res.format_diff(context=1))

def lnhashview_msg(
    id, # Message id, looked up in `dlg` (unique prefixes allowed)
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Hash-addressed view of a message's content, for `msg_exhash`"
    return _to_dlg(dlg).msg(id).lnhashview()

def msg_exhash(
    id, # Message id, looked up in `dlg` (unique prefixes allowed)
    *cmds:tuple, # exhash command tuples, addresses from `lnhashview_msg`
    sw:int=4, # Shift width for indent commands
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Apply exhash commands to a message in the dialog file, returning the diff"
    d = _to_dlg(dlg)
    res = d.msg(id).exhash(*cmds, sw=sw)
    _save(d)
    return res

# %% ../nbs/05_dlgskill.ipynb #38af2f2e
def add_msg(
    source:str, # source for the new message
    msg_type:str='code', # 'code', 'note', 'prompt', or 'raw'
    before:str=None, # message or id to insert before
    after:str=None, # message or id to insert after
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Add a new message before/after an existing one (pass exactly one), returning it"
    d, sv = _load_dlg(dlg)
    m = d.mk_message(source, msg_type=msg_type,
        before=None if before is None else d.msg(before), after=None if after is None else d.msg(after))
    _save(d, sv)
    return m

def del_msgs(
    *ids, # Messages or ids to delete
    dlg=None, # An ipynb path; the current dialog file if None
):
    "Delete messages by id, returning the removed messages"
    d, sv = _load_dlg(dlg)
    res = Msgs(d.remove_msgs([d.msg(i) for i in ids]))
    _save(d, sv)
    return res

def create_dlg(
    fname:str, # path for the new ipynb; must not already exist
    source:str='', # source for its first message
    msg_type:str='code', # 'code', 'note', 'prompt', or 'raw'
):
    "Create a new dialog file containing one message, returning the `Dialog` (with `path_` stamped)"
    f = Path(fname)
    if f.exists(): raise FileExistsError(str(f))
    d = Dialog(name=f.stem)
    d.mk_message(source, msg_type=msg_type)
    write_ipynb(d, f)
    d.path_ = f
    return d

# %% ../nbs/05_dlgskill.ipynb #fb670f10
def add_msg_magic(line, cell):
    "Add a new message with the magic body as its source, taken verbatim."
    kw = {}
    for t in shlex.split(line):
        if '=' in t: kw.update([t.split('=', 1)])
        elif t in smsg_types: kw.setdefault('msg_type', t)
        else: kw.setdefault('dlg', t)
    return add_msg(cell.rstrip('\n'), **kw)

def load_ipython_extension(ipython): ipython.register_magic_function(add_msg_magic, 'cell', 'add_msg')

try:
    from IPython import get_ipython
    if (_ip := get_ipython()): load_ipython_extension(_ip)
except ImportError: pass
