((raw_block
  name: (raw_block_name) @_name
  content: (raw_content) @injection.content)
  (#eq? @_name "body:json")
  (#set! injection.language "json"))

((raw_block
  name: (raw_block_name) @_name
  content: (raw_content) @injection.content)
  (#eq? @_name "body:graphql")
  (#set! injection.language "graphql"))

((raw_block
  name: (raw_block_name) @_name
  content: (raw_content) @injection.content)
  (#eq? @_name "body:graphql:vars")
  (#set! injection.language "json"))

((raw_block
  name: (raw_block_name) @_name
  content: (raw_content) @injection.content)
  (#eq? @_name "body:xml")
  (#set! injection.language "xml"))

((raw_block
  name: (raw_block_name) @_name
  content: (raw_content) @injection.content)
  (#eq? @_name "script:pre-request")
  (#set! injection.language "javascript"))

((raw_block
  name: (raw_block_name) @_name
  content: (raw_content) @injection.content)
  (#eq? @_name "script:post-response")
  (#set! injection.language "javascript"))

((raw_block
  name: (raw_block_name) @_name
  content: (raw_content) @injection.content)
  (#eq? @_name "tests")
  (#set! injection.language "javascript"))

((raw_block
  name: (raw_block_name) @_name
  content: (raw_content) @injection.content)
  (#eq? @_name "docs")
  (#set! injection.language "markdown"))
