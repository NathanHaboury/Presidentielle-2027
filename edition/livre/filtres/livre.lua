--[[
Filtre du livre (Quarto). Il adapte au livre les dossiers, écrits pour GitHub.
Les fichiers Markdown ne sont pas modifiés : tout se passe au moment du rendu.

1. Ancres. Les liens internes des dossiers suivent les ancres de GitHub
   (« #4-ce-que-le-parallele-apprend »). Pandoc fabrique d'autres ancres, et
   le PDF réunit tous les chapitres dans un seul document, où « #sources »
   existe douze fois. Le filtre donne donc à chaque titre une ancre unique,
   <fichier>--<ancre GitHub>, et réécrit les liens de la même façon. Un lien
   vers une ancre introuvable devient du texte simple.

2. Liens vers des fichiers hors du livre (charte, audit…) : ils pointent vers
   le fichier sur GitHub.

3. Titres de niveau 1 en trop. Certains dossiers ont des « Partie A / Partie B »
   de niveau 1. Dans le livre, le niveau 1 est réservé au titre du chapitre :
   ces parties descendent d'un niveau, et leurs sous-titres aussi.

4. Sections retirées du livre (elles restent sur GitHub) : « Sommaire »
   (le livre a sa table des matières) et « À vérifier » (outil de travail
   du glossaire).

5. Graphiques : le titre est déjà dans l'image (charte, section 5). Le texte
   alternatif n'est donc pas répété en légende sous le graphique.

6. Tableaux : les largeurs de colonnes calculées par Pandoc (égales, d'après
   les tirets de l'en-tête) sont retirées ; la mise en page les ajuste au contenu.
]]

local REPO = "https://github.com/NathanHaboury/Presidentielle-2027/blob/main/"
local DROP = { "^Sommaire", "^Table des matières", "^À vérifier" }

-- Décodage base64 (métadonnées que Quarto glisse avant chaque chapitre).
local B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
local function b64decode(data)
  data = data:gsub("[^" .. B64 .. "=]", "")
  return (data:gsub(".", function(x)
    if x == "=" then return "" end
    local r, f = "", (B64:find(x, 1, true) - 1)
    for i = 6, 1, -1 do r = r .. (f % 2 ^ i - f % 2 ^ (i - 1) > 0 and "1" or "0") end
    return r
  end):gsub("%d%d%d?%d?%d?%d?%d?%d?", function(x)
    if #x ~= 8 then return "" end
    local c = 0
    for i = 1, 8 do c = c + (x:sub(i, i) == "1" and 2 ^ (8 - i) or 0) end
    return string.char(c)
  end))
end

local function chapter_file(block)
  if block.t ~= "RawBlock" then return nil end
  local enc = block.text:match("quarto%-file%-metadata:%s*([A-Za-z0-9+/=]+)")
  if not enc then return nil end
  return b64decode(enc):match('"bookItemFile"%s*:%s*"([^"]+)"')
end

-- Ancre à la manière de GitHub.
local function github_slug(text)
  local s = pandoc.text.lower(text)
  local out = {}
  for _, c in utf8.codes(s) do
    if c == 32 then
      out[#out + 1] = "-"
    elseif (c >= 48 and c <= 57) or (c >= 97 and c <= 122) or c == 45 or c == 95
        or (c >= 0xC0 and c <= 0x24F and c ~= 0xD7 and c ~= 0xF7) then
      out[#out + 1] = utf8.char(c)
    end
  end
  return table.concat(out)
end

local function stem(path)
  local name = path:match("([^/\\]+)$") or path
  return (name:gsub("%.[^.]+$", ""))
end

local function dirname(path)
  return path:match("^(.*)/[^/]*$") or ""
end

-- « finances-publiques/../energie/x.md » → « energie/x.md »
local function normalize(path)
  local parts = {}
  for part in path:gmatch("[^/]+") do
    if part == ".." then
      if #parts > 0 then table.remove(parts) end
    elseif part ~= "." then
      parts[#parts + 1] = part
    end
  end
  return table.concat(parts, "/")
end

-- Fichiers du livre, lus dans _quarto.yml (liste « render »).
local function book_files(project_dir)
  local files = {}
  local f = io.open((project_dir or ".") .. "/_quarto.yml", "r")
  if not f then return files end
  for line in f:lines() do
    local p = line:match("^%s*%-%s+([%w%._/%-]+%.q?md)%s*$")
    if p then files[p] = true end
  end
  f:close()
  return files
end

local function project_dir()
  if quarto and quarto.project and quarto.project.directory then
    return quarto.project.directory
  end
  return "."
end

local function current_file()
  local input = (quarto and quarto.doc and quarto.doc.input_file)
    or (PANDOC_STATE and PANDOC_STATE.input_files and PANDOC_STATE.input_files[1])
    or "document.md"
  local dir = project_dir()
  if dir and input:sub(1, #dir + 1) == dir .. "/" then
    input = input:sub(#dir + 2)
  end
  return input
end

local function is_boundary(b)
  if b.t == "RawBlock" and chapter_file(b) then return true end
  if b.t == "Div" and (b.classes:includes("quarto-book-part") or b.classes:includes("hidden")) then
    return true
  end
  return false
end

-- 5. Graphiques sans légende répétée.
function Figure(fig)
  local images = {}
  fig.content:walk({ Image = function(img) images[#images + 1] = img end })
  if #images ~= 1 then return nil end
  local img = images[1]
  local alt = pandoc.utils.stringify(img.caption)
  if alt == "" then alt = pandoc.utils.stringify(fig.caption.long) end
  img.caption = {}
  img.attributes["fig-alt"] = alt
  return pandoc.Para({ img })
end

-- 6. Tableaux : largeurs ajustées au contenu. Une colonne reçoit au moins la
-- place de son mot le plus long ; le reste est partagé selon la longueur
-- moyenne du texte des cases. Les petits tableaux gardent la mise en page
-- automatique.
local LINE = 100 -- caractères sur une ligne de tableau, environ

local function cell_text(cell)
  return pandoc.utils.stringify(cell.contents)
end

function Table(tbl)
  local n = #tbl.colspecs
  local sum, count, longest = {}, {}, {}
  for i = 1, n do sum[i], count[i], longest[i] = 0, 0, 0 end
  local function scan(rows)
    for _, row in ipairs(rows) do
      for i, cell in ipairs(row.cells) do
        if i <= n then
          local t = cell_text(cell)
          sum[i] = sum[i] + utf8.len(t)
          count[i] = count[i] + 1
          for w in t:gmatch("%S+") do
            longest[i] = math.max(longest[i], utf8.len(w) or #w)
          end
        end
      end
    end
  end
  scan(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do scan(body.body) end

  local mins, wants, total_want, total_min = {}, {}, 0, 0
  for i = 1, n do
    local mean = count[i] > 0 and sum[i] / count[i] or 0
    mins[i] = math.min(math.max(longest[i] + 2, 8), 30)
    wants[i] = math.max(mean, mins[i])
    total_want = total_want + wants[i]
    total_min = total_min + mins[i]
  end

  local widths = {}
  if total_want <= LINE * 0.6 then
    for i = 1, n do widths[i] = nil end -- petit tableau : automatique
  elseif total_want <= LINE then
    for i = 1, n do widths[i] = wants[i] / total_want end
  else
    local rest = math.max(LINE - total_min, 0)
    local extra = total_want - total_min
    for i = 1, n do
      local w = mins[i] + (extra > 0 and rest * (wants[i] - mins[i]) / extra or 0)
      widths[i] = w / math.max(LINE, total_min)
    end
  end
  for i, cs in ipairs(tbl.colspecs) do
    tbl.colspecs[i] = { cs[1], widths[i] or pandoc.ColWidthDefault }
  end
  return tbl
end

function Pandoc(doc)
  local files = book_files(project_dir())

  -- Passe 1 : découper en chapitres, retirer les sections, ajuster les niveaux,
  -- poser les ancres.
  local out = pandoc.Blocks({})
  local file = current_file()
  local seen_h1 = false   -- le titre du chapitre a-t-il été vu ?
  local seen_sub = false  -- un titre de niveau 2 ou plus a-t-il été vu ?
  local shift = 0         -- décalage des niveaux après une « Partie » de niveau 1
  local skipping = false
  local known = {}

  for _, b in ipairs(doc.blocks) do
    local f = chapter_file(b)
    if f then
      file, seen_h1, seen_sub, shift = f, false, false, 0
    end
    if is_boundary(b) then skipping = false end

    if b.t == "Header" then
      -- Le premier titre de niveau 1, avant toute section, est le titre du
      -- chapitre. (Dans le site, Quarto l'a déjà retiré du texte : un niveau 1
      -- qui suit une section est donc toujours une « Partie ».)
      if b.level == 1 and not seen_h1 and not seen_sub then
        seen_h1, shift = true, 0
      elseif b.level == 1 then
        seen_h1, shift = true, 1
      else
        seen_sub = true
      end
      if b.level <= 2 then
        skipping = false
        local title = pandoc.utils.stringify(b.content)
        if b.level == 2 or (b.level == 1 and shift == 1) then
          for _, p in ipairs(DROP) do
            if title:match(p) then skipping = true end
          end
        end
      end
      if not skipping and not (b.level == 1 and shift == 0) then
        local slug = github_slug(pandoc.utils.stringify(b.content))
        if slug ~= "" then
          local id = stem(file) .. "--" .. slug
          if known[id] then
            local n = 1
            while known[id .. "-" .. n] do n = n + 1 end
            id = id .. "-" .. n
          end
          known[id] = true
          b.identifier = id
        end
        b.level = math.min(b.level + shift, 6)
      end
    end

    if not skipping then out:insert(b) end
  end

  -- Passe 2 : réécrire les liens, chapitre par chapitre.
  local combined = false
  local count = 0
  for _, b in ipairs(out) do
    if chapter_file(b) then count = count + 1 end
  end
  combined = count > 1

  file = current_file()
  local result = pandoc.Blocks({})
  for _, b in ipairs(out) do
    local f = chapter_file(b)
    if f then file = f end
    local here = file
    local nb = pandoc.walk_block(b, {
      Link = function(l)
        local t = l.target
        if t:match("^%a[%w+.-]*:") then return nil end -- http:, mailto:…
        local path, anchor = t:match("^([^#]*)#?(.*)$")
        if path == "" then
          if anchor == "" then return nil end
          local id = stem(here) .. "--" .. anchor
          if known[id] then
            l.target = "#" .. id
            return l
          end
          return pandoc.Span(l.content)
        end
        if not path:match("%.q?md$") then return nil end
        local target = normalize(dirname(here) .. "/" .. path)
        if not files[target] then
          l.target = REPO .. target .. (anchor ~= "" and ("#" .. anchor) or "")
          return l
        end
        if anchor == "" then return nil end
        local id = stem(target) .. "--" .. anchor
        if combined and not known[id] then
          l.target = path -- ancre introuvable : lien vers le chapitre
        else
          l.target = path .. "#" .. id
        end
        return l
      end
    })
    result:insert(nb)
  end
  doc.blocks = result
  return doc
end
