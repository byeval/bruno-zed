; Redact likely secret values during collaboration/screen sharing.

((pair
  key: (_) @_key
  value: (_) @redact)
  (#match? @_key "(?i)(authorization|token|secret|password|passwd|api[-_]?key|access[-_]?key|client[-_]?secret|session[-_]?token)"))

((pair
  key: (quoted_key) @_key
  value: (_) @redact)
  (#match? @_key "(?i)(authorization|token|secret|password|passwd|api[-_]?key|access[-_]?key|client[-_]?secret|session[-_]?token)"))
