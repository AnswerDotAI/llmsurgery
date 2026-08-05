"Plumbing shared by the session modules; not generated from a notebook"

from fastcore.utils import Path

__all__ = ['uniq_path']

def uniq_path(
    paths, # Candidate paths, e.g. from a glob
    ref, # The reference they were matched against, for the error message
):
    "The single path in `paths`, or None if there are none; raises if `ref` is ambiguous"
    res = sorted({str(o) for o in paths})
    if len(res)>1: raise ValueError(f'{ref!r} matches {len(res)} sessions:\n' + '\n'.join(res))
    return Path(res[0]) if res else None
