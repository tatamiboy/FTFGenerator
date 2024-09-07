------------------------------------------------------------------------------------
-- globals
------------------------------------------------------------------------------------
_chapterExportDir = ""
_chapterOverwrite = false

  -- 方向指定. FTFGのインデックスと順番を揃える
_chapterDirectionIdx = {txtTopBottom,
                        txtBottomTop,
                        txtRightLeft,
                        txtLeftRight,
                        txtTopRightBottomLeft,
                        txtBottomLeftTopRight,
                        txtBottomRightTopLeft,
                        txtTopLeftBottomRight}

---言語切り替え---
_lang = "en" 

---初期化---
function init()
  print("initialized")
end

---GUIを閉じても実行される---
function update(delta)
end

---GUI---
function gui()
  ---チャプターを作成---
  if _lang == "jp" then
    txtTitle = "チャプターを作成"
    txtExportdir = "保存先"
    txtOverwrite = "上書きする"
    txtExport = "保存"
    txtStart = "チャプター開始(100-0)"
    txtEnd = "チャプター終了"
    txtEndFailed = "チャプター終了を設定できませんでした。チャプター開始が正しくありません。"
    txtTopBottom = "上-下"
    txtBottomTop = "下-上"
    txtRightLeft = "右-左"
    txtLeftRight = "左-右"
    txtTopRightBottomLeft = "右上-左下"
    txtBottomLeftTopRight = "左下-右上"
    txtBottomRightTopLeft = "右下-左上"
    txtTopLeftBottomRight = "左上-右下"
    txtFailed = "保存できませんでした。ログを確認してください。"
    tooltipTxt = "FPTFGenerator用チャプターファイルを作成します。"
    tooltipTxtStart = "現在位置にチャプター開始点をセットします。"
    tooltipTxtEnd = "現在位置にチャプター終了点をセットします"
  else
    txtTitle = "Create chapters"
    txtExportdir = "Export destination"
    txtOverwrite = "Overwrite if existing."
    txtExport = "Export"
    txtStart = "Chapter start(100-0)"
    txtEnd = "Chapter end"
    txtEndFailed = "Could not set chapter end. Bad chapter start."
    txtTopBottom = "Top-Bottom"
    txtBottomTop = "Bottom-Top"
    txtRightLeft = "Right-Left"
    txtLeftRight = "Left-Right"
    txtTopRightBottomLeft = "Top Right-Bottom Left"
    txtBottomLeftTopRight = "Bottom Left-Top Right"
    txtBottomRightTopLeft = "Bottom Right-Top Left"
    txtTopLeftBottomRight = "Top Left-Bottom Right"
    txtFailed = "Failed to export. Please check the log."
    tooltipTxt = "Create a chapter file for the FPTFGenerator. Set the chapter start to 0 and the chapter end to 100."
    tooltipTxtStart = "Sets the chapter start at the current position."
    tooltipTxtEnd = "Sets the chapter end at the current position."
  end

  ofs.Text(txtTitle)
  ofs.Tooltip(tooltipTxt)
  _chapterExportDir = ofs.Input(txtExportdir, _chapterExportDir)
  _chapterOverwrite = ofs.Checkbox(txtOverwrite, _chapterOverwrite)

  ofs.Text(txtStart)
  ofs.Tooltip(tooltipTxtStart)
  btnTopBottom = ofs.Button(txtTopBottom)
  ofs.SameLine()
  btnBottomTop = ofs.Button(txtBottomTop)
  ofs.SameLine()
  btnRightLeft = ofs.Button(txtRightLeft)
  ofs.SameLine()
  btnLeftRight = ofs.Button(txtLeftRight)
  btnTopRightBottomLeft = ofs.Button(txtTopRightBottomLeft)
  ofs.SameLine()
  btnBottomLeftTopRight = ofs.Button(txtBottomLeftTopRight)
  btnBottomRightTopLeft = ofs.Button(txtBottomRightTopLeft)
  ofs.SameLine()
  btnTopLeftBottomRight = ofs.Button(txtTopLeftBottomRight)

  ofs.NewLine()
  ofs.Text(txtEnd)
  ofs.Tooltip(tooltipTxtEnd)
  btnEnd = ofs.Button(txtEnd)

  if btnTopBottom then
    binding.setStartPoint(0)
  elseif btnBottomTop then
    binding.setStartPoint(1)
  elseif btnRightLeft then
    binding.setStartPoint(2)
  elseif btnLeftRight then
    binding.setStartPoint(3)
  elseif btnTopRightBottomLeft then
    binding.setStartPoint(4)
  elseif btnBottomLeftTopRight then
    binding.setStartPoint(5)
  elseif btnBottomRightTopLeft then
    binding.setStartPoint(6)
  elseif btnTopLeftBottomRight then
    binding.setStartPoint(7)
  elseif btnEnd then
    if not binding.setEndPoint() then
      print(txtEndFailed)
    end
  end

  ofs.NewLine()
  if ofs.Button(txtExport) then
    local result, message = binding.createChapter()
    if not result then txtInfo = txtFailed
    else txtInfo = message end
  end
  ofs.Text(txtInfo)
end


---関数---

function binding.setStartPoint(dir)
  local script = ofs.Script(ofs.ActiveIdx())
  local time = player.CurrentTime() 

  local closestAct, idx = script:closestAction(time)
  if closestAct and time < closestAct.at + 0.01 and closestAct.at - 0.01 < time then
    script:markForRemoval(idx)
    script:removeMarked() 
    script:commit()
  end

  -- 前のチャプターが閉じているか確認
  local closestBefAct = script:closestActionBefore(time)
  if closestBefAct and closestBefAct.pos % 10 ~= 9 then
    return false
  end

  print("add")
  script.actions:add(Action.new(time, dir * 10))
  script:commit()
 end

function binding.setEndPoint()
  local script = ofs.Script(ofs.ActiveIdx())
  local time = player.CurrentTime() 

  -- 前の点があるか確認.
  local closestBefAct = script:closestActionBefore(time)
  if not closestBefAct then
    return false
  end

  -- 重なる点があったら警告.
  local closestAct, idx = script:closestAction(time)
  if closestAct and time < closestAct.at + 0.01 and closestAct.at - 0.01 < time then
    print("Points are too close.")
    return false
  end

  print(closestBefAct.pos % 10)
  -- 前の点がチャプター開始点か確認
  if closestBefAct.pos % 10 ~= 0 then
    return false
  else 
    script.actions:add(Action.new(time, closestBefAct.pos + 9))
    script:commit()
    return true
  end
end


function exists(file)
   local ok, err, code = os.rename(file, file)
   if not ok then
      if code == 13 then
         return false
      end
   end
   return ok, err
end

---チャプターファイルを作成---
function binding.createChapter()

  local txtChapterNotClosed
  local txtFileExist
  if _engMode == false then
    txtChapterNotClosed = "エラー:チャプターが閉じていません。"
    txtFileExist = "エラー:同名ファイルが存在するか、保存先に書き込めません。"
    txtExportFailed = "エラー:保存できませんでした。"
  else
    txtChapterNotClosed = "Error: A file with the same name exists or the destination cannot be written to."
    txtFileExist = "Error: A file with the same name exists."
    txtExportFailed = "Error: Export failed."
  end

  local script = ofs.Script(ofs.ActiveIdx())
  local chapterStartAt, chapterEndAt, dir = {}, {}, {}
  local lastPos = -1

  for  idx, action in ipairs(script.actions) do
    if action.pos % 10 == 0 then
      table.insert(chapterStartAt, action.at)
      lastPos = 0
    elseif lastPos == 0 then
      table.insert(chapterEndAt, action.at)
      table.insert(dir, math.floor(action.pos / 10))
      lastPos = 9
    end
  end

  -- チャプターが閉じてない場合
  if #chapterStartAt ~= #chapterEndAt then
    print(txtChapterNotClosed)
    return false
  end

  -- 保存先ディレクトリの末尾に区切り文字をつける
  if string.sub(_chapterExportDir, -1) ~= package.config:sub(1,1) then
    _chapterExportDir = (_chapterExportDir..package.config:sub(1,1))
  end

  local exportFilePath = _chapterExportDir..ofs.ScriptName(ofs.ActiveIdx())..".txt"
  print("File: "..exportFilePath)

  -- 同名チャプターファイルがある場合
  if (not _chapterOverwrite) and exists(exportFilePath) then
    print(txtFileExist)
    return false
  end

  local file, err = io.open(exportFilePath, "w")
  if file then
    for idx, val in ipairs(chapterStartAt) do
      print(val..":"..chapterEndAt[idx]..":"..dir[idx])
      file:write(val..":"..chapterEndAt[idx]..":"..dir[idx], "\n")
    end
    file:close()
  else
    print(txtExportFailed)
    print(err)
    return false
  end
  return true, exportFilePath
end
