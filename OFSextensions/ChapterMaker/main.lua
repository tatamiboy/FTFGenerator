------------------------------------------------------------------------------------
-- globals
------------------------------------------------------------------------------------
---言語切り替え---
_lang = "en" 

_chapterExportDir = ""
_chapterOverwrite = false

  -- 方向指定. FTFGのインデックスと順番を揃える
_chapterDirectionIdx = {_txtTopBottom,
                        _txtBottomTop,
                        _txtRightLeft,
                        _txtLeftRight,
                        _txtTopRightBottomLeft,
                        _txtBottomLeftTopRight,
                        _txtBottomRightTopLeft,
                        _txtTopLeftBottomRight}

if _lang == "jp" then
  _txtTitle = "チャプターを作成"
  _txtExportdir = "保存先"
  _txtOverwrite = "上書きする"
  _txtExport = "保存"
  _txtStart = "チャプター開始(100-0)"
  _txtEnd = "チャプター終了"
  _txtEndFailed = "エラー: チャプター終了を設定できませんでした。チャプター開始が正しくありません。"
  _txtTopBottom = "上-下"
  _txtBottomTop = "下-上"
  _txtRightLeft = "右-左"
  _txtLeftRight = "左-右"
  _txtTopRightBottomLeft = "右上-左下"
  _txtBottomLeftTopRight = "左下-右上"
  _txtBottomRightTopLeft = "右下-左上"
  _txtTopLeftBottomRight = "左上-右下"
  _txtFailed = "エラー: 保存できませんでした。ログを確認してください。"
  _tooltipTxt = "FPTFGenerator用チャプターファイルを作成します。"
  _tooltipTxtStart = "現在位置にチャプター開始点をセットします。"
  _tooltipTxtEnd = "現在位置にチャプター終了点をセットします"
  _txtChapterNotClosed = "エラー:チャプターが閉じていません。"
  _txtPreviousChapterNotClosed = "エラー:前のチャプターが閉じていません。"
  _txtFileExist = "エラー:同名ファイルが存在するか、保存先に書き込めません。"
  _txtPointsTooClose = "情報: 頂点が近すぎます。"
else
  _txtTitle = "Create chapters"
  _txtExportdir = "Export destination"
  _txtOverwrite = "Overwrite if existing."
  _txtExport = "Export"
  _txtStart = "Chapter start(100-0)"
  _txtEnd = "Chapter end"
  _txtEndFailed = "Error: Could not set chapter end. Bad chapter start."
  _txtTopBottom = "Top-Bottom"
  _txtBottomTop = "Bottom-Top"
  _txtRightLeft = "Right-Left"
  _txtLeftRight = "Left-Right"
  _txtTopRightBottomLeft = "Top Right-Bottom Left"
  _txtBottomLeftTopRight = "Bottom Left-Top Right"
  _txtBottomRightTopLeft = "Bottom Right-Top Left"
  _txtTopLeftBottomRight = "Top Left-Bottom Right"
  _txtFailed = "Error: Failed to export. Please check the log."
  _tooltipTxt = "Create a chapter file for the FPTFGenerator. Set the chapter start to 0 and the chapter end to 100."
  _tooltipTxtStart = "Sets the chapter start at the current position."
  _tooltipTxtEnd = "Sets the chapter end at the current position."
  _txtChapterNotClosed = "Error: The chapter is not closed."
  _txtPreviousChapterNotClosed = "Error: Previous chapter not closed"
  _txtFileExist = "Error: A file with the same name exists or the destination cannot be written to."
  _txtPointsTooClose = "Info: Points are too close."
end


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
  ofs.Text(_txtTitle)
  ofs.Tooltip(_tooltipTxt)
  _chapterExportDir = ofs.Input(_txtExportdir, _chapterExportDir)
  _chapterOverwrite = ofs.Checkbox(_txtOverwrite, _chapterOverwrite)

  ofs.Text(_txtStart)
  ofs.Tooltip(_tooltipTxtStart)
  btnTopBottom = ofs.Button(_txtTopBottom)
  ofs.SameLine()
  btnBottomTop = ofs.Button(_txtBottomTop)
  ofs.SameLine()
  btnRightLeft = ofs.Button(_txtRightLeft)
  ofs.SameLine()
  btnLeftRight = ofs.Button(_txtLeftRight)
  btnTopRightBottomLeft = ofs.Button(_txtTopRightBottomLeft)
  ofs.SameLine()
  btnBottomLeftTopRight = ofs.Button(_txtBottomLeftTopRight)
  btnBottomRightTopLeft = ofs.Button(_txtBottomRightTopLeft)
  ofs.SameLine()
  btnTopLeftBottomRight = ofs.Button(_txtTopLeftBottomRight)

  ofs.Text(_txtEnd)
  ofs.Tooltip(_tooltipTxtEnd)
  btnEnd = ofs.Button(_txtEnd)

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
      print(_txtEndFailed)
    end
  end

  if ofs.Button(_txtExport) then
    local result, message = binding.createChapter()
    if not result then _txtInfo =_txtFailed
    else _txtInfo = message end
  end
  ofs.Text(_txtInfo)
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

  script.actions:add(Action.new(time, dir * 10))
  script:commit()
 end

function binding.setEndPoint()
  local script = ofs.Script(ofs.ActiveIdx())
  local time = player.CurrentTime() 

  -- 前の点があるか確認.
  local closestBefAct = script:closestActionBefore(time)
  if not closestBefAct then
    print(_txtPreviousChapterNotClosed)
    return false
  end

  -- 重なる点があったら警告.
  local closestAct, idx = script:closestAction(time)
  if closestAct and time < closestAct.at + 0.01 and closestAct.at - 0.01 < time then
    print(_txtPointsTooClose)
    return false
  end

  -- 前の点がチャプター開始点か確認
  if closestBefAct.pos % 10 ~= 0 then
    print(_txtPreviousChapterNotClosed)
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
    print(_txtChapterNotClosed)
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
    print(_txtFileExist)
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
    print(err)
    return false
  end
  return true, exportFilePath
end
