; Show Zed runnable controls for Bruno request blocks.
; The task binding lives in languages/bru/tasks.json and can be overridden
; from a project or global tasks.json with the same "bruno-request" tag.

(
  (request_block
    name: (request_block_name) @run)
  (#set! tag bruno-request)
)
