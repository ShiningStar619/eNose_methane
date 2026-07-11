-- Pandoc filter: callouts + รูป + คำบรรยาย (สำหรับ export Word)

local function is_caption(para)
  if para.t ~= "Para" or #para.content ~= 1 then
    return false
  end
  local inline = para.content[1]
  return inline.t == "Emph" or inline.t == "Strong"
end

local function has_image(para)
  if para.t ~= "Para" then
    return false
  end
  for _, inline in ipairs(para.content) do
    if inline.t == "Image" then
      return true
    end
  end
  return false
end

function BlockQuote(bq)
  local text = pandoc.utils.stringify(bq)
  if text:match("^สำคัญ:") then
    return pandoc.Div(bq.content, {["custom-style"] = "Callout Important"})
  end
  if text:match("^หมายเหตุ:") then
    return pandoc.Div(bq.content, {["custom-style"] = "Callout Note"})
  end
  return bq
end

function Image(img)
  if img.src:match("%.svg$") then
    img.src = img.src:gsub("%.svg$", ".png")
  end
  return img
end

function Blocks(blocks)
  local out = {}
  local i = 1
  while i <= #blocks do
    local block = blocks[i]
    if has_image(block) and i < #blocks and is_caption(blocks[i + 1]) then
      local cap = pandoc.utils.stringify(blocks[i + 1])
      table.insert(out, pandoc.Div(
        { block, pandoc.Para({ pandoc.Str(cap) }) },
        { ["custom-style"] = "Figure Block" }
      ))
      i = i + 2
    else
      table.insert(out, block)
      i = i + 1
    end
  end
  return out
end
