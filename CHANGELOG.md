# Release notes

<!-- do not remove -->

## 0.0.4

### New Features

- Expand Codex session support (read/write/build rollouts, custom tools, thread↔dialog round-trip), add locked headless subagent runner, and support dotted tool names + lnhash view in dialog editing ([#7](https://github.com/AnswerDotAI/llmsurgery/issues/7))
- Add compact DSL and synthetic session compaction; replace synthetic ant fixtures with real Claude Code transcripts; add structural search predicates, session naming/resolution, and Dialog↔Message backrefs ([#6](https://github.com/AnswerDotAI/llmsurgery/issues/6))
- Add `reads_ipynb` for reading dialogs from JSON strings ([#3](https://github.com/AnswerDotAI/llmsurgery/pull/3)), thanks to [@jackhogan](https://github.com/jackhogan)


## 0.0.3

### New Features

- `split_msg`: drop `parts` param and absorb one `\n\n` at each cut for byte-exact merge round-trip ([#5](https://github.com/AnswerDotAI/llmsurgery/issues/5))


## 0.0.2

### New Features

- Rename dlg2canon→dlg2chat and msgs2hist→dlg2hist, add sections/headers, kernel output streaming, exported-code property, expanduser paths, and session system-record round-tripping ([#4](https://github.com/AnswerDotAI/llmsurgery/issues/4))


## 0.0.1

### New Features

- Add `append_sess` to chain records onto an existing session tail; misc style cleanups ([#1](https://github.com/AnswerDotAI/llmsurgery/issues/1))

