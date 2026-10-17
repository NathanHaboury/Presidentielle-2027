--[[
Notes de source (filtre commun au livre Quarto et aux PDF des chapitres).

Dans les dossiers, une même source est appelée plusieurs fois avec la même
étiquette, par exemple [^insee-2106]. GitHub n'affiche alors qu'une note,
avec plusieurs renvois. Pandoc, lui, crée une note par appel : une source
citée dix fois donnerait dix notes identiques. Deux notes sont « la même »
si leur contenu est identique.

- PDF du livre (Typst) : les notes ne sont pas en bas de page. Chaque appel
  devient un numéro en exposant, cliquable, et les notes sont regroupées à la
  fin du chapitre, sous « Notes de source ». Une même source garde un seul
  numéro. La numérotation repart de 1 à chaque chapitre (titre de niveau 1).
- HTML (site du livre, PDF des chapitres) : la première note de chaque source
  est gardée ; les appels suivants deviennent un lien vers elle, avec le même
  numéro. Le regroupement se fait aussi chapitre par chapitre.
]]

local TITRE_NOTES = "Notes de source"

local function cle(note)
  return pandoc.write(pandoc.Pandoc(note.content), "native")
end

-- PDF (Typst) : notes en fin de chapitre ----------------------------------

local function bloc_notes(notes, chapitre)
  local blocs = pandoc.List()
  local h = pandoc.Header(2, pandoc.Inlines(TITRE_NOTES), pandoc.Attr("", { "unnumbered", "unlisted" }))
  blocs:insert(h)
  blocs:insert(pandoc.RawBlock("typst", "#[\n#set text(size: 8.5pt)\n#set par(spacing: 0.75em, first-line-indent: 0pt)"))
  for i, contenu in ipairs(notes) do
    local tete = pandoc.Inlines({
      pandoc.RawInline("typst", "#metadata(none) <fnt-" .. chapitre .. "-" .. i .. ">"),
      pandoc.Strong(pandoc.Inlines(tostring(i) .. ".")),
      pandoc.Space(),
    })
    local premier = contenu[1]
    if premier and (premier.t == "Para" or premier.t == "Plain") then
      blocs:insert(pandoc.Para(tete .. premier.content))
      for j = 2, #contenu do
        blocs:insert(contenu[j])
      end
    else
      blocs:insert(pandoc.Para(tete))
      blocs:extend(contenu)
    end
  end
  blocs:insert(pandoc.RawBlock("typst", "]"))
  return blocs
end

local function notes_en_fin(doc)
  local sortie = pandoc.List()
  local chapitre = 0
  local numero, notes = {}, {}

  local function vider()
    if #notes > 0 then
      sortie:extend(bloc_notes(notes, chapitre))
    end
    numero, notes = {}, {}
  end

  local remplacer = {
    Note = function(note)
      local k = cle(note)
      local i = numero[k]
      if i == nil then
        notes[#notes + 1] = note.content
        i = #notes
        numero[k] = i
      end
      return pandoc.RawInline("typst",
        "#super[#link(<fnt-" .. chapitre .. "-" .. i .. ">)[" .. i .. "]]")
    end,
  }

  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 1 then
      vider()
      chapitre = chapitre + 1
      sortie:insert(b)
    else
      sortie:insert(pandoc.walk_block(b, remplacer))
    end
  end
  vider()
  doc.blocks = sortie
  return doc
end

-- HTML : une note par source --------------------------------------------

local function notes_regroupees(doc)
  local numero = {}
  local n = 0
  return doc:walk({
    traverse = "topdown",
    Header = function(h)
      if h.level == 1 then
        numero = {}
      end
    end,
    Note = function(note)
      local k = cle(note)
      local i = numero[k]
      if i == nil then
        n = n + 1
        numero[k] = n
        return note, false
      end
      return pandoc.RawInline("html",
        '<a href="#fn' .. i .. '" class="footnote-ref" role="doc-noteref"><sup>' .. i .. '</sup></a>'), false
    end,
  })
end

function Pandoc(doc)
  if FORMAT:match("typst") then
    return notes_en_fin(doc)
  elseif FORMAT:match("html") then
    return notes_regroupees(doc)
  end
  return nil
end
