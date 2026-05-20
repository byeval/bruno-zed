; Show Zed runnable controls for Bruno YAML request files.
; This augments Zed's built-in YAML language without changing ordinary YAML
; unless the document has Bruno's top-level `http:` request shape.

(
  (block_mapping_pair
    key: (flow_node) @run
    value: (block_node
      (block_mapping
        (block_mapping_pair
          key: (flow_node) @_method_key)
        (block_mapping_pair
          key: (flow_node) @_url_key))))
  (#eq? @run "http")
  (#eq? @_method_key "method")
  (#eq? @_url_key "url")
  (#set! tag bruno-yaml-request)
)
