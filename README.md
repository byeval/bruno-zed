# Bruno for Zed

First-stage Bruno support for Zed:

- `.bru` language registration
- Tree-sitter parser for Bru request files
- Syntax highlighting for blocks, pairs, disabled entries, variables, files, booleans, numbers, strings, and comments
- Language injections for JSON, GraphQL, XML, JavaScript, and Markdown raw blocks
- Runnable markers on HTTP request blocks
- Bruno YAML runnable markers for `.yml` / `.yaml` request files that use Bruno's `http:` request shape
- Zed task templates that call `bru run`
- Redaction rules for likely secrets
- POSIX helper script for resolving a request file to its Bruno collection root

## Layout

```text
.
├── extension.toml
├── bin
│   ├── bru-zed-run
│   └── bru-zed-yaml-run
├── languages/bru
│   ├── config.toml
│   ├── highlights.scm
│   ├── injections.scm
│   ├── runnables.scm
│   ├── redactions.scm
│   └── tasks.json
├── languages/yaml
│   ├── config.toml
│   ├── highlights.scm
│   ├── runnables.scm
│   └── tasks.json
├── tree-sitter-bru
│   ├── grammar.js
│   ├── queries/highlights.scm
│   └── src/parser.c
└── bin/bru-zed-run
```

## Install Locally

1. Open Zed.
2. Run `zed: extensions`.
3. Click `Install Dev Extension`.
4. Choose `/Volumes/iDev/workspace/side/bruno-zed`.

The grammar is currently referenced through:

```toml
[grammars.bru]
repository = "https://github.com/byeval/tree-sitter-bru"
rev = "5ed48a02b69dd4021742a7982c2606e638852317"
```

For local grammar development, clone `https://github.com/byeval/tree-sitter-bru`
into this repository as `tree-sitter-bru` or update `extension.toml` temporarily.

## CLI Task

Install Bruno CLI if you want `.bru` runnable tasks to execute real requests:

```sh
npm install -g @usebruno/cli
```

With a `.bru` file open, Zed should show a runnable on the request method block, such as `get`, `post`, or `http`. With a Bruno YAML request open, Zed should show the runnable on the `http:` block when it contains a method and URL.

The default task searches upward from the current file until it finds `bruno.json` or `opencollection.yml`. For `bruno.json` collections, it delegates to Bruno CLI:

```sh
bru run <relative-request-path>
```

For `opencollection.yml` YAML collections, Bruno CLI 1.16.0 does not currently recognize the root or run `.yml` requests, so the extension uses `bin/bru-zed-yaml-run` as a first-stage HTTP runner. It supports the common HTTP request fields, including method, URL, headers, query params, and `form-urlencoded`, `json`, `text`, `xml`, `html`, or simple multipart bodies.

The helper script can be tested outside Zed:

```sh
BRU=echo ./bin/bru-zed-run examples/basic-collection/ping.bru --env Local
./bin/bru-zed-run /path/to/collection/request.yml --dry-run
```

Expected output:

```text
run ping.bru --env Local
```

## Development

Install grammar dependencies:

```sh
cd tree-sitter-bru
npm install
```

Generate and test:

```sh
cd /Volumes/iDev/workspace/side/bruno-zed
npm run check
```

Parse examples:

```sh
cd tree-sitter-bru
npm run parse -- ../examples/kitchen-sink.bru
```

## Current Limits

- This is not a full Bruno GUI inside Zed. Zed currently lacks a VS Code-style WebView/custom activity panel API for recreating Bruno's full request editor.
- The parser is editor-oriented, not a replacement for Bruno's official Ohm parser.
