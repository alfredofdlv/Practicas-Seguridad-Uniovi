-- CONSEJO/IMPORTANTE -> cajas; tablas ASCII -> Table; arboles -> caja monospace; resto -> caja codigo.

local function get_classes(block)
  if block.attr and block.attr.classes then
    return block.attr.classes
  end
  return {}
end

local function lines_of(text)
  local lines = {}
  for line in (text .. "\n"):gmatch("(.-)\r?\n") do
    if line:match("%S") then
      table.insert(lines, line)
    end
  end
  return lines
end

local function split_cols(line)
  local cols, pos = {}, 1
  while pos <= #line do
    local gap = line:find("%s%s+", pos)
    if not gap then
      local rest = line:sub(pos):match("^%s*(.-)%s*$")
      if rest ~= "" then
        table.insert(cols, rest)
      end
      break
    end
    local cell = line:sub(pos, gap - 1):match("^%s*(.-)%s*$")
    if cell ~= "" then
      table.insert(cols, cell)
    end
    pos = gap
    while pos <= #line and line:sub(pos, pos):match("%s") do
      pos = pos + 1
    end
  end
  return cols
end

local function is_tree(text)
  return text:match("[├└│]") ~= nil
end

local function is_ascii_table(text)
  if is_tree(text) then
    return false
  end
  local lines = lines_of(text)
  if #lines < 2 then
    return false
  end
  local ncol = nil
  for _, line in ipairs(lines) do
    local cols = split_cols(line)
    if #cols < 2 then
      return false
    end
    if not ncol then
      ncol = #cols
    elseif #cols ~= ncol then
      return false
    end
  end
  return ncol ~= nil and ncol >= 2
end

local function latex_escape(s)
  s = s:gsub("\\", "\\textbackslash{}")
  s = s:gsub("([%%$&#_{}])", "\\%1")
  return s
end

local function colspec_for(ncol)
  return string.rep("l", ncol)
end

local function header_cells(header)
  local cells = {}
  for _, c in ipairs(header) do
    table.insert(cells, "\\textcolor{tableheadtext}{\\bfseries " .. latex_escape(c) .. "}")
  end
  return cells
end

local function ascii_table_latex(text)
  local lines = lines_of(text)
  local header = split_cols(lines[1])
  local ncol = #header
  local colspec = colspec_for(ncol)

  local out = {}
  table.insert(out, "\\begin{tablebox}")
  table.insert(out, "\\renewcommand{\\arraystretch}{1.25}")
  table.insert(out, "\\begin{tabular}{" .. colspec .. "}")
  table.insert(out, "\\toprule")
  table.insert(out, table.concat(header_cells(header), " & ") .. " \\\\")
  table.insert(out, "\\midrule")

  for i = 2, #lines do
    local cols = split_cols(lines[i])
    local cells = {}
    for j = 1, ncol do
      table.insert(cells, latex_escape(cols[j] or ""))
    end
    table.insert(out, table.concat(cells, " & ") .. " \\\\")
  end
  table.insert(out, "\\bottomrule")

  table.insert(out, "\\end{tabular}")
  table.insert(out, "\\end{tablebox}")
  return pandoc.RawBlock("latex", table.concat(out, "\n") .. "\n")
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
  local body = pandoc.write(pandoc.Pandoc(text_to_blocks(text)), "latex")
  return pandoc.RawBlock("latex", "\\begin{" .. env .. "}\n" .. body .. "\\end{" .. env .. "}\n")
end

local function wrap_verbatim_box(env, text)
  return pandoc.RawBlock(
    "latex",
    "\\begin{" .. env .. "}\n\\begin{Verbatim}[breaklines,fontsize=\\small]\n"
      .. text
      .. "\n\\end{Verbatim}\n\\end{" .. env .. "}\n"
  )
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
  if is_ascii_table(text) then
    return ascii_table_latex(text)
  end
  if is_tree(text) then
    return wrap_verbatim_box("treebox", text)
  end

  return wrap_verbatim_box("codebox", text)
end

