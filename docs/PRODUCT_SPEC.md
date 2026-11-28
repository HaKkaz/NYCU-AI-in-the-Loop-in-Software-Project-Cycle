# 開發決策時間軸：產品規格

> **修改方式：** 開 PR 修改本文件，並在 DECISIONS.md 記一筆。不要只在聊天裡改口。

---

## 0. 給開發者與 Agent 的閱讀規則

1. **本文件是產品行為的唯一依據。** 程式碼、issue 或對話內容和本文件衝突時，先停下來問人，不要自己選一邊。
2. **標記的意思：**
   - `[已決定]`：團隊已經同意，不可以自行更改。
   - `[預設]`：目前照這樣做，但團隊還沒正式拍板。可以照著實作，不要擴大範圍。
   - `[待決]`：還沒決定，見 §16。遇到時請問人，不要自己決定。
3. **不要主動加入 §3.2「不做的事」裡列的功能。**
4. 規格寫「必須」的地方，要有對應的測試。
5. 實作時如果發現規格寫不清楚，請開 issue 或在 PR 裡提出，不要自行補上假設。

---

## 1. 產品一句話

把 GitHub repo 裡的 **DECISIONS.md 決策**和 **Pull Request** 排在同一條時間軸上。做功能的人把決策連到相關 PR，接手的人確認這條關聯或提出疑問。這樣交接時不用重新翻紀錄、也不用一直問人，就能知道「這個 PR 是為了哪個決策做的」。

## 2. 問題與使用者

### 2.1 目標使用者

用 GitHub 協作的小型開發團隊（2–6 人），例如課堂專題或黑客松隊伍。

### 2.2 要解決的問題

決策寫在 DECISIONS.md，實作分散在好幾個 PR，討論又留在聊天群組裡。單看其中一個地方，資訊都不完整：

| 只看這裡 | 缺什麼 |
|---|---|
| Commit／PR | 知道改了什麼，不知道是為了哪個決策；一個需求拆成多個 PR 時，要自己串起來 |
| DECISIONS.md | 知道為什麼，不知道最後改在哪個 PR |
| 聊天群組 | 問得到當事人時很快，但換一個人接手就要再問一次 |

### 2.3 使用情境

- **交接**：A 做完一段，B 休息回來要接手。
- **Review**：審查者想知道這個 PR 是為了哪個決策。
- **回顧**：事後想查某個決策最後落在哪些 PR。

### 2.4 來自使用者訪談的設計原則（CP1 §2.2）

- **P1 回到原文：** 點一個決策就要能看到相關 PR，而且能看到原始內容，不能只顯示整理過的一句結論。
- **P2 先連再確認：** 做功能的人先建立關聯，由另一個人確認。沒有人檢查過的關聯，不能看起來像是已經確認的答案。

## 3. 範圍

### 3.1 第一版要做的事

- 讀取一個 GitHub **公開** repo 的 DECISIONS.md 和 PR
- 把決策和 PR 依時間排成一條時間軸
- 查看決策與 PR 的原文，並能開啟 GitHub 原始連結
- 用拖曳把決策連到 PR，一個決策可以連多個 PR
- 對關聯做確認、提出疑問、回應、撤回，並記錄是誰做的
- 兩個人同時使用時，看到同一份資料（透過輪詢同步）

### 3.2 第一版不做的事

- 寫回 GitHub：不改 DECISIONS.md、不在 PR 留言、不加 label
- 私有 repo、GitHub OAuth 登入
- 任何 AI 功能，包括自動推薦或摘要（見 §13）
- 在本工具裡編輯決策內容（決策一律在 DECISIONS.md 寫）
- 分析 commit（只處理 PR）
- 通知（email、Slack、推播）
- 即時游標、WebSocket
- 手機版拖曳操作
- 同時處理多個 repo

## 4. 名詞

| 名詞 | 程式名稱 | 意思 |
|---|---|---|
| 決策 | `Decision` | DECISIONS.md 裡的一筆紀錄。只讀，每次從檔案解析 |
| PR | `PullRequest` | GitHub 上的 Pull Request。只讀 |
| 關聯 | `Link` | 「某個決策 ↔ 某個 PR」的一條連線，由使用者建立，存在資料庫 |
| 建立者 | `created_by` | 建立這條關聯的人 |
| 操作者 | `actor` | 送出這次操作的人（名字） |
| 狀態 | `status` | 關聯目前的狀態，見 §7 |
| 事件 | `LinkEvent` | 關聯的每一次狀態變化，用來顯示歷程 |

## 5. 核心流程：兩人交接

| 步驟 | 誰 | 做什麼 | 系統行為 |
|---|---|---|---|
| 1 | 系統 | 讀進 DECISIONS.md 和 PR | 依時間排出節點 |
| 2 | A | 把決策拖到相關 PR，可以連好幾個 | 每條關聯建立為 `pending` |
| 3 | B | 點開決策與 PR 原文，確認看懂原因、沒有連錯或漏連 | 只讀 |
| 4 | B → A | 有問題就對那條關聯提出疑問；A 回應或撤回 | `pending → disputed → pending`，或撤回 |
| 5 | B | 沒問題就確認 | `pending → confirmed` |

**這個流程成功的標準（CP1 §4.1）：** B 不靠 A 口頭說明，就能找到對應的 PR，並用自己的話說出這個決策的原因。

## 6. 功能需求

每一條都有編號，PR 和測試請引用編號，例如 `F4`。

### F1 載入 repo

- 目標 repo 由環境變數 `GITHUB_REPO` 設定，格式為 `owner/name`。`[預設]`
- 讀取 default branch 根目錄的 `DECISIONS.md`。
- 讀取 PR 的範圍：已合併的 PR 和 open 的 PR；關閉但未合併的不顯示。`[預設]`
- GitHub 回應快取 10 分鐘。`GET /api/timeline?refresh=1` 可以略過快取。
- 有設定 `GITHUB_TOKEN` 就帶上 token；沒有設定也要能運作。

**驗收：**
- 遇到 rate limit 或 GitHub 連不上時，API 回 `503`，`detail` 說明原因，例如 `GitHub rate limit reached, resets at 14:05`。不可以回 500。
- 找不到 DECISIONS.md 時，仍然顯示 PR，並在 `warnings` 中說明。

### F2 時間軸

- 決策和 PR 顯示在同一條時間軸上，依時間排序。
  - 決策用 `date`。
  - PR 用 `merged_at`；還沒合併的用 `created_at`，並且標示「未合併」。
  - 同一天的決策排在 PR 前面。
- 決策節點和 PR 節點的外觀必須能區分。
- 決策節點上要顯示各狀態的關聯數量，例如「2 已確認 · 1 待確認」。

### F3 內容區

- 點決策：顯示 `title`、`date`、`what`、`why`、`led_by`，以及原始 Markdown 片段（P1）。
- 點 PR：顯示編號、標題、作者、時間、內文，以及開啟 GitHub 的連結。
- 兩種節點都要列出相關的所有關聯，以及各自的狀態與歷程。

### F4 建立關聯

- 把決策節點拖到 PR 節點上就會建立關聯。
- 同一組（決策, PR）只能有一條有效的關聯。重複建立回 `409`。
- 新的關聯狀態是 `pending`，`created_by` 是操作者。
- 決策或 PR 不存在時回 `404`。

### F5–F8 關聯操作

規則完整寫在 §7 的狀態機。摘要如下：

- **F5 確認：** 建立者以外的人可以確認。
- **F6 提出疑問：** 必須留言，讓建立者知道哪裡有問題。
- **F7 回應：** 建立者回覆疑問後，關聯回到 `pending`，等待再次確認。
- **F8 撤回：** 只有建立者可以撤回自己建立的關聯。連錯 PR 的修正方式是「撤回後重新建立」。

### F9 歷程

每條關聯都要能看到完整歷程：誰在什麼時候做了什麼，以及留言內容。

### F10 同步

- 前端每 5 秒呼叫一次 `GET /api/timeline`。`[預設]`
- 一個人做的變更，另一個人最晚 5 秒後（加上請求時間）就要看到。
- 使用者正在拖曳或輸入留言時，輪詢結果不可以打斷操作或清掉輸入內容。

### F11 身分

- 第一次開啟時輸入名字，存在瀏覽器的 localStorage。`[預設]`
- 每個寫入請求都帶上 `actor`。
- 不做驗證，名字可以被冒用。這是已知限制（§14）。

## 7. 關聯狀態機

狀態：`pending`（待確認）、`confirmed`（已確認）、`disputed`（有疑問）、`withdrawn`（已撤回，不顯示在時間軸上）。

| 目前狀態 | 動作 `action` | 誰可以做 | 結果 | 留言 |
|---|---|---|---|---|
| （不存在） | `create` | 任何人 | `pending` | 選填 |
| `pending` | `confirm` | 建立者以外的人 | `confirmed` | 選填 |
| `pending` | `dispute` | 建立者以外的人 | `disputed` | **必填** |
| `pending` | `withdraw` | 建立者 | `withdrawn` | 選填 |
| `disputed` | `respond` | 建立者 | `pending` | **必填** |
| `disputed` | `withdraw` | 建立者 | `withdrawn` | 選填 |
| `confirmed` | `dispute` | 任何人 | `disputed` | **必填** |

**必須遵守的規則：**

1. 表格以外的組合一律回 `409`，`detail` 說明為什麼不允許。例如 `Link creator cannot confirm their own link`。
2. 留言必填時，空字串或只有空白一律回 `422`。
3. 權限檢查必須在後端做。前端隱藏按鈕只是為了方便操作，不能取代後端檢查。
4. 每一次狀態變化都要寫一筆 `LinkEvent`，包括 `create`。
5. `withdrawn` 是終止狀態，不能再變回其他狀態。撤回後，同一組（決策, PR）可以重新建立。
6. 不提供硬刪除。

這部分的邏輯集中在 `backend/app/links/transitions.py`，而且每一列都要有對應的測試。

## 8. 資料模型

### Decision（每次解析，不存）

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | `str` | `{date}-{slug(title)}`。slug 規則見 §9。同一個 id 重複時加上 `-2`、`-3` |
| `date` | `date` | |
| `title` | `str` | |
| `what` | `str` | |
| `why` | `str` | |
| `led_by` | `str \| None` | |
| `raw` | `str` | 這筆紀錄的原始 Markdown（P1） |

### PullRequest（只快取，不存）

| 欄位 | 型別 |
|---|---|
| `number` | `int` |
| `title` | `str` |
| `body` | `str` |
| `author` | `str` |
| `state` | `"open" \| "merged"` |
| `created_at` | `datetime` |
| `merged_at` | `datetime \| None` |
| `url` | `str` |

### Link（SQLite）

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | `int` | |
| `decision_id` | `str` | 對應 `Decision.id` |
| `pr_number` | `int` | |
| `status` | `"pending" \| "confirmed" \| "disputed" \| "withdrawn"` | |
| `created_by` | `str` | |
| `created_at` | `datetime` | UTC |
| `updated_at` | `datetime` | UTC |

同一組（`decision_id`, `pr_number`）在 `status != "withdrawn"` 的範圍內必須唯一。

### LinkEvent（SQLite）

| 欄位 | 型別 |
|---|---|
| `id` | `int` |
| `link_id` | `int` |
| `actor` | `str` |
| `action` | `"create" \| "confirm" \| "dispute" \| "respond" \| "withdraw"` |
| `comment` | `str \| None` |
| `at` | `datetime`（UTC） |

所有時間在 API 中一律以 ISO 8601 UTC 傳遞，由前端轉成使用者的時區顯示。

## 9. DECISIONS.md 解析規則

本專案自己的 DECISIONS.md 就是主要的測試資料。

```markdown
## 2026-09-21 — Initial code steward
**What:** Alex is the initial code steward for the team.
**Why:** volunteered
**Led by:** Alex
```

- 每一筆從 `## YYYY-MM-DD <分隔符> 標題` 開始。分隔符接受 `—`、`–`、`-`。
- 欄位用 `**What:**`、`**Why:**`、`**Led by:**` 開頭。欄位內容可以跨好幾行，直到下一個欄位或下一個 `##` 為止。
- 不認得的欄位（例如 `**Alternative rejected:**`）保留在 `raw` 裡，不另外解析。
- 缺少 `What` 或 `Why` 的紀錄仍然要解析出來，缺的欄位給空字串，並加一筆 warning。
- 日期格式錯誤的紀錄跳過，並加一筆 warning。**解析錯誤不可以讓整個 API 失敗。**
- slug 的規則：轉成小寫，保留英文字母、數字和中日韓文字，其他字元換成 `-`，連續的 `-` 合併成一個，頭尾的 `-` 去掉。

## 10. API

所有 API 都在 `/api` 之下。FastAPI 自動產生的 `/docs` 是格式的實際參考。如果 `/docs` 和本節不一致，以本節為準，並修正程式。

### `GET /api/timeline`

Query：`refresh=1`（選填，略過 GitHub 快取）

```json
{
  "repo": "owner/name",
  "generated_at": "2026-11-28T09:00:00Z",
  "decisions": [Decision],
  "pull_requests": [PullRequest],
  "links": [Link & { "events": [LinkEvent] }],
  "warnings": ["DECISIONS.md line 42: invalid date '2026-13-01'"]
}
```

`links` 不包含 `withdrawn` 的關聯。

### `POST /api/links`

```json
{ "decision_id": "2026-09-21-initial-code-steward", "pr_number": 3, "actor": "Alex", "comment": null }
```

成功回 `201` 和 `Link`。決策或 PR 不存在回 `404`；重複建立回 `409`。

### `PATCH /api/links/{id}`

```json
{ "action": "dispute", "actor": "Sam", "comment": "PR #3 只改了文件，實作在 #5" }
```

成功回 `200` 和更新後的 `Link`（含 `events`）。關聯不存在回 `404`；不允許的轉換回 `409`；缺少必填留言回 `422`。

### 錯誤格式

一律使用 FastAPI 預設的 `{"detail": "..."}`。`detail` 用英文寫，要說明哪裡錯、怎麼修正。

## 11. 介面需求

- 畫面分成三區：**時間軸**、**內容區**、**關聯狀態**（CP1 §3.3）。
- 狀態不能只靠顏色區分，必須同時有文字標籤（待確認／已確認／有疑問）。
- 按鈕只在使用者有權限時顯示，例如建立者看不到自己關聯的「確認」按鈕。但後端仍然要檢查（§7 規則 3）。
- 提出疑問和回應時，留言框是空的就不能送出。
- 空狀態：沒有決策、沒有 PR、還沒有任何關聯時，都要顯示說明文字，告訴使用者下一步做什麼。
- API 錯誤要把 `detail` 顯示給使用者，不可以靜默失敗。
- 介面文字使用繁體中文。

## 12. 非功能需求

| 項目 | 要求 |
|---|---|
| 規模 | 最多 200 個 PR、100 筆決策、同時 5 個人使用 |
| 效能 | 有快取時，`GET /api/timeline` 在 1 秒內回應 |
| 瀏覽器 | 桌面版 Chrome、Firefox、Safari 的最新版本 |
| 機密 | `GITHUB_TOKEN` 只從環境變數讀取，不可以 commit，也不可以印在 log 裡 |
| 資料庫 | 由 `DATABASE_URL` 設定，預設是 `sqlite:///./data/app.db`。`data/` 加入 `.gitignore` |
| 測試 | 後端使用 pytest。§7 狀態機的每一列、§9 的每一條解析規則都要有測試 |

## 13. AI 的邊界

- **第一版產品不包含任何 AI 功能。** `[預設]` 在 CP2 繳交時要聲明這一點。
- 如果之後加入 AI，它只能**建議**候選關聯：建立的關聯一律是 `pending`，`created_by` 寫成 `ai:<model>`，而且不能執行 `confirm`（CP1 §4.3）。
- 本節是「產品功能裡的 AI」。團隊開發時使用 AI 工具的規則，寫在 AI 使用守則裡，不在這份文件。

## 14. 已知限制

把這些限制寫進評估報告，不需要在第一版解決：

1. 改了 DECISIONS.md 的標題或日期，`Decision.id` 就會改變，舊的關聯會對不上。這類關聯在 `warnings` 中列出。
2. 身分沒有驗證，可以冒用別人的名字。
3. 輪詢最多有 5 秒的延遲。
4. 只讀 default branch 的 DECISIONS.md。
5. 沒有 token 時，GitHub 限制每小時 60 次請求。

## 15. 技術架構

| 項目 | 選擇 | 狀態 |
|---|---|---|
| 後端 | FastAPI（Python） | `[已決定]` |
| 前端 | React + Vite（JavaScript） | `[預設]` |
| 前端部署 | build 後由 `app.frontend("/", directory=...)` 提供（FastAPI ≥ 0.141） | `[預設]` |
| 資料庫 | SQLite + Python 標準函式庫 sqlite3 | `[預設]` |
| 同步 | 每 5 秒輪詢 | `[預設]` |
| GitHub | REST API，使用 httpx | `[預設]` |

```
backend/app/
  main.py               建立 app、掛上 /api 路由、app.frontend()
  models.py             Pydantic API 輸入輸出模型（§8）
  github/               解析 DECISIONS.md、抓 PR、合併時間軸（F1、F2、§9）
  links/                db.py 共用 sqlite3 連線、migrate.py 遷移、store.py 讀寫、transitions.py 狀態機
  routers/              timeline.py、links.py（§10）
backend/migrations/     依序執行的 SQL 檔案，資料表定義的唯一來源
backend/tests/
frontend/src/           Timeline、ContentPanel、LinkStatus、api.js（F2、F3、F10、§11）
```

開發時前後端分開跑：`fastapi dev`（:8000）和 `npm run dev`（:5173，`/api` 轉給 :8000）。Demo 時先 `npm run build`，再用 `fastapi run` 跑單一服務。

## 16. 待決事項

遇到這些問題時，請問團隊，不要自己決定：

- [ ] 要不要顯示關閉但未合併的 PR？（目前不顯示）
- [ ] 要不要解析 PR 內文裡的 `Decision:` 欄位，自動視為該 PR 的決策？（目前不解析）
- [ ] 身分要不要改用 GitHub 帳號？（目前輸入名字）
- [ ] 決策改標題後，要不要提供把舊關聯重新對應的方法？（目前只列在 warnings）

## 17. 變更紀錄

| 版本 | 日期 | 內容 |
|---|---|---|
| v0.1 | 2026-11-28 | 初稿：依 CP1 與 CP2 架構討論整理 |
| v0.2 | 2026-11-29 | 資料庫實作用標準函式庫 sqlite3，schema 由編號 SQL migration 維護。 |
