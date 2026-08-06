# Release notes

<!-- do not remove -->

## 0.0.11

### New Features

- Make `openai_codex` and json5 imports optional in oai module so it degrades gracefully when those packages are not installed ([#27](https://github.com/AnswerDotAI/llmsurgery/issues/27))


## 0.0.10

### New Features

- Add session mirror module for ipynb transcript indexing, plus per-message provenance meta and dedup/fallback record handling ([#26](https://github.com/AnswerDotAI/llmsurgery/issues/26))
- Migrate to aidialog typed message parts (Text/Thinking/ToolUse/ToolResult) replacing Part/PartType ([#25](https://github.com/AnswerDotAI/llmsurgery/issues/25))
- Add llmsurgery.sess: cross-host session lookup by id prefix and dialog reading, with sess2nb CLI ([#24](https://github.com/AnswerDotAI/llmsurgery/issues/24))
- Guard session chains against uuid cycles/duplicates, accept bare `mcp__` tool names in dialogs, and drop dlg2thread ([#23](https://github.com/AnswerDotAI/llmsurgery/issues/23))


## 0.0.9

### New Features

- Add dlg2compact flat-document projection and table-driven `call_renderers` dispatch ([#22](https://github.com/AnswerDotAI/llmsurgery/issues/22))
- Move hist module from llmsurgery to aidialog ([#21](https://github.com/AnswerDotAI/llmsurgery/issues/21))
- Point session-reading docs at dialogs first, and make search hits `L`-based with sized truncation previews ([#20](https://github.com/AnswerDotAI/llmsurgery/issues/20))

### Bugs Squashed

- Fix CI: add tiktoken to required dependencies ([#14](https://github.com/AnswerDotAI/llmsurgery/pull/14)), thanks to [@ncoop57](https://github.com/ncoop57)
- add missing deps ([#11](https://github.com/AnswerDotAI/llmsurgery/pull/11)), thanks to [@RensDimmendaal](https://github.com/RensDimmendaal)


## 0.0.8

### New Features

- Use the message model from aidialog rather than fastllm ([#19](https://github.com/AnswerDotAI/llmsurgery/pull/19)), thanks to [@jph00](https://github.com/jph00)
- Refactor tool-call wire format: replace details-block parsing with `strip_tools`, simplify JSON tool schema ([#18](https://github.com/AnswerDotAI/llmsurgery/issues/18))


## 0.0.7

### New Features

- Move hist and compact modules into llmsurgery, replace antskill with unified skill entry point, and add Codex `web_search_call` support ([#17](https://github.com/AnswerDotAI/llmsurgery/issues/17))


## 0.0.6

### New Features

- Migrate to aidialog ([#16](https://github.com/AnswerDotAI/llmsurgery/issues/16))
- Add tool deferral, deferred-session resume, and stream-event query support to ant module ([#13](https://github.com/AnswerDotAI/llmsurgery/issues/13))
- Add `incl_out`/`trunc_out` to message views and normalize `parse_exec` MCP tail matching across Codex versions ([#12](https://github.com/AnswerDotAI/llmsurgery/issues/12))
- Replace hand-rolled Codex app-server client with `openai_codex` SDK, add synthetic thread compaction, normalize LaTeX in AI rendering, and make Dialog iterable ([#10](https://github.com/AnswerDotAI/llmsurgery/issues/10))


## 0.0.5

### New Features

- Split dlgskill into transactional file functions and in-memory session methods; reorder Dialog(name=) keyword, add MsgRow snapshots, rename hist `to_xml`→`hist_xml` and `exhash_msg`→`msg_exhash`, replace `python_msgs`/`ast_msgs` with `msg_ast_replace` ([#8](https://github.com/AnswerDotAI/llmsurgery/issues/8))


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
