; Bruno/Bru syntax highlighting.

(comment) @comment

[
  "{"
  "}"
  "["
  "]"
] @punctuation.bracket
(disabled_marker) @operator

(request_block
  name: (request_block_name) @function.method)

(block
  name: (block_name) @keyword)

(raw_block
  name: (raw_block_name) @keyword)

(pair
  key: (_) @property)

(annotation) @attribute

(template_variable) @variable.special

(file_reference) @string.special

(content_type_annotation) @attribute

[
  (double_quoted_string)
  (single_quoted_string)
] @string

(number) @number
(boolean) @boolean
(null) @constant.builtin

(bare_value_chunk) @string
(bare_list_value) @string.special
(raw_line) @embedded
