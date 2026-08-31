--[[
  shunn.lua — pandoc filter for Shunn manuscript format
  https://www.shunn.net/format/story/

  Normalises the manuscript's own conventions into the structural elements
  that shunn.latex knows how to typeset:

    * H1  "Chapter IX - The Fjord"  ->  \chapteropening{...} (new page, dropped)
    * H2  "~ * ~" / "~ *** ~"       ->  \scenebreak (a centred #)
    * bare "~ * ~" lines that pandoc mis-parses as definition lists
                                    ->  the paragraph above + \scenebreak
    * fenced code (screen text)     ->  \machinetext{...}, centred, body font
    * ::: theend :::                ->  \theend (a centred # # #)

  Metadata read:
    classic  — true to underline emphasis (Shunn Classic) instead of italics
]]

local stringify = pandoc.utils.stringify

local classic = false
local saw_end_marker = false
local chapter_count = 0

local function raw(s)
  return pandoc.RawBlock('latex', s)
end

-- Render inlines to a LaTeX string so titles keep their emphasis and get
-- escaped correctly, without pandoc inserting \par inside a macro argument.
local function inlines_to_latex(inlines)
  local doc = pandoc.Pandoc({ pandoc.Plain(inlines) })
  return (pandoc.write(doc, 'latex'):gsub('%s+$', ''))
end

local function escape_latex(s)
  return (s:gsub('([\\{}$&#^_~%%])', {
    ['\\'] = '\\textbackslash{}',
    ['{']  = '\\{',
    ['}']  = '\\}',
    ['$']  = '\\$',
    ['&']  = '\\&',
    ['#']  = '\\#',
    ['^']  = '\\textasciicircum{}',
    ['_']  = '\\_',
    ['~']  = '\\textasciitilde{}',
    ['%']  = '\\%',
  }))
end

-- A divider is a line made only of ornament characters: ~ * # - – — • ·
local function is_divider(s)
  s = s:gsub('%s', '')
  return s ~= '' and s:match('^[~%*#%-–—•·]+$') ~= nil
end

local read_meta = {
  Meta = function(meta)
    classic = meta.classic == true or stringify(meta.classic or '') == 'true'
    return meta
  end
}

local cleanup = {
  -- manuscript/10_Phil.md carries stray U+2028/U+2029 separators from a word
  -- processor. No text font has a glyph for them; treat them as spaces.
  Str = function(el)
    local fixed = el.text:gsub('\u{2028}', ' '):gsub('\u{2029}', ' ')
    if fixed ~= el.text then return pandoc.Str(fixed) end
    return nil
  end
}

local underline_emphasis = {
  Emph = function(el)
    if not classic then return nil end
    return { pandoc.RawInline('latex', '\\uline{') }
      .. el.content
      .. { pandoc.RawInline('latex', '}') }
  end
}

local structure = {
  Header = function(el)
    if is_divider(stringify(el.content)) then
      return raw('\\scenebreak')
    end
    if el.level == 1 then
      chapter_count = chapter_count + 1
      local macro = (chapter_count == 1) and '\\firstchapteropening'
                                          or '\\chapteropening'
      return raw(macro .. '{' .. inlines_to_latex(el.content) .. '}')
    end
    -- Any surviving subheading (e.g. the appendix's "Maps") is centred plain.
    return raw('\\subheading{' .. inlines_to_latex(el.content) .. '}')
  end,

  -- Chapter III writes its dividers as bare "~ * ~" lines, which pandoc reads
  -- as a definition list hanging off the preceding paragraph. Undo that.
  DefinitionList = function(el)
    local out = {}
    for _, item in ipairs(el.content) do
      local term, defs = item[1], item[2]
      local all_dividers = #defs > 0
      for _, blocks in ipairs(defs) do
        if not is_divider(stringify(blocks)) then all_dividers = false end
      end
      if not all_dividers then return nil end -- a real definition list; leave it
      table.insert(out, pandoc.Para(term))
      table.insert(out, raw('\\scenebreak'))
    end
    return out
  end,

  -- Fenced blocks in this manuscript are machine/screen text, not code.
  CodeBlock = function(el)
    local lines = {}
    for line in (el.text .. '\n'):gmatch('(.-)\n') do
      line = line:match('^%s*(.-)%s*$')
      if line ~= '' then table.insert(lines, escape_latex(line)) end
    end
    if #lines == 0 then return {} end
    -- \\[0pt] rather than \\ : a bare \\ would scan ahead and eat the leading
    -- asterisk of the next line ("*** ALL ..." -> "** ALL ...") as \\*.
    return raw('\\machinetext{' .. table.concat(lines, '\\\\[0pt]\n') .. '}')
  end,

  Div = function(el)
    if el.classes:includes('theend') then
      saw_end_marker = true
      return raw('\\theend')
    end
    return nil
  end,

  -- If the build didn't place an explicit end marker, close the manuscript.
  Pandoc = function(doc)
    if not saw_end_marker then
      doc.blocks:insert(raw('\\theend'))
    end
    return doc
  end
}

return { read_meta, cleanup, underline_emphasis, structure }
