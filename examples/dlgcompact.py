#!/usr/bin/env python
"Write a one-cell compacted copy of a dialog, as `<name>-comp.ipynb`."
from fastcore.script import call_parse
from fastcore.utils import Path
from aidialog.dialog import Dialog, sraw
from aidialog.ipynb import read_ipynb, write_ipynb
from llmsurgery.compact import dlg2compact, len_toks

@call_parse
def main(
    fname:str,  # Dialog ipynb to compact
    user_toks:int=None, asst_toks:int=None, call_toks:int=None, result_toks:int=None,  # Per-message token budgets; `compact_policy` if None
):
    "Write `fname`'s compacted text as a single raw cell in `<fname>-comp.ipynb`"
    src = Path(fname)
    d = read_ipynb(src)
    txt = dlg2compact(d, user_toks, asst_toks, call_toks, result_toks)
    out = src.with_name(src.stem + '-comp' + src.suffix)
    res = Dialog(name=out.stem)
    res.mk_message(txt, msg_type=sraw)
    write_ipynb(res, out)
    print(f'{out}: {len(d.messages)} messages, {len_toks(txt)} tokens')
