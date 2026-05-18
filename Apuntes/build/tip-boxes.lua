-- Convierte bloques de codigo sin lenguaje que empiezan por CONSEJO/IMPORTANTE en cajas LaTeX.

local function get_classes(block)
  if block.attr and block.attr.classes then
    return block.attr.classes
  end
  return {}
end

local function text_to_blocks(text)
  local blocks = {}
  for line in (text .. "\n"):gmatch("(.-)\r?\n") do
    table.insert(blocks, pandoc.Para({ pandoc.Str(line) }))
  end
  if #blocks == 0 then
    blocks = { pandoc.Para({ pandoc.Str(text) }) }
  end
  return blocks
end

local function wrap_box(env, text)
  local body = pandoc.write(
    pandoc.Pandoc(text_to_blocks(text)),
    "latex"
  )
  return pandoc.RawBlock("latex", "\\begin{" .. env .. "}\n" .. body .. "\\end{" .. env .. "}\n")
end

function CodeBlock(block)
  if #get_classes(block) > 0 then
    return nil
  end

  local text = block.text or ""
  if text:match("^CONSEJO:") then
    return wrap_box("consejo", text)
  end
  if text:match("^IMPORTANTE") then
    return wrap_box("importante", text)
  end

  return nil
end
