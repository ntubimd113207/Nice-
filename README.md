# Nice巴底
**組    別：第113207組**  

**專題名稱：Nice巴底**  
  
**指導教授：林宏仁 老師**  
  
**專題學生：11236024 楊翊萍、11236026 陳妤瑄、10856042 楊喬羽、10856004 葉千熏**  
  
___
## 前言  
### 背景介紹  
　　在台灣十大死因裡，其中就有五項跟飲食密切相關，因此Nice巴底的誕生致力於幫助人們實現「健康飲食」目標，而訓練有素的「AI營養師」則結合飲食法、個人喜好與食材預算，提供美味且營養的食譜。
  
　　「巴底」取自「Body」與「Buddy」的諧音，除了期許人們能擁有健康的身體外，同時也希望成為支持大家執行這些行動的"好夥伴"。
### 動機
　　現在健康意識抬頭，讓人們更重視日常飲食習慣，然而，研究與設計適合的食譜又相當耗時，對非專業人士來說是一個極大的挑戰。因此，Nice巴底希望能讓更多人輕鬆實行健康飲食，從而更好地顧及到身體健康。
### 系統目的與目標
- 透過AI營養師快速獲得符合需求的健康食譜，節省大量時間和精力。
- 促進健康飲食習慣的養成，降低飲食相關疾病的風險，提升人們整體生活質量和健康狀況。
- 紀錄與展示健康成果，使自身的努力可視化，增加成就感並促進長期健康習慣的養成。
- 營造互助的健康飲食環境，透過發布貼文、分享經驗和創意，讓使用者互相鼓勵和支持。
### 預期成果
- 吸引更多人嘗試和維持健康飲食習慣，提升國民整體健康水準。
- 在獲取食譜的過程中，可吸收到關於營養和健康的知識，提高他們對飲食選擇的認識，長期受益。
## 系統規格
### 系統架構
![photo_2024-09-21_16-20-58](https://github.com/user-attachments/assets/553cb068-7af0-41c8-93e1-a54cd67d6de5)
### 系統架構 - 樹狀圖
![photo_2024-09-21_16-31-47](https://github.com/user-attachments/assets/4f7a4eeb-968a-41de-bc92-3012b95e4954)
### 系統軟、硬體需求與技術平台
<table>
  <tr>
    <th colspan="2">硬體需求</th>
  </tr>
  <tr>
    <td>作業系統</td>
    <td>Windows、Mac</td>
  </tr>
</table>  
<table>
  <tr>
    <th colspan="2">裝置需求</th>
  </tr>
  <tr>
    <td>網路需求</td>
    <td>WiFi/行動數據</td>
  </tr>
  <tr>
    <td>網頁需求</td>
    <td>建議使用Chrome</td>
  </tr>
</table>  

### 使用標準與工具
<table>
  <tr>
    <th colspan="2">系統開發環境</th>
  </tr>
  <tr>
    <td>作業系統</td>
    <td>Windows</td>
  </tr>
  <tr>
    <td>撰寫工具</td>
    <td>Visual Studio Code、DBeaver</td>
  </tr>
</table>  
<table>
  <tr>
    <th colspan="2">程式開發語言</th>
  </tr>
  <tr>
    <td>前端</td>
    <td>HTML、CSS、JS</td>
  </tr>
  <tr>
    <td>後端</td>
    <td>Flask</td>
  </tr>
  <tr>
    <td>資料庫</td>
    <td>PostgreSQL</td>
  </tr>
</table>  
<table>
  <tr>
    <th colspan="2">介面及插圖繪製工具</th>
  </tr>
  <tr>
    <td>插圖</td>
    <td>Copilot、DALL-E</td>
  </tr>
  <tr>
    <td>介面</td>
    <td>Figma</td>
  </tr>
</table> 
<table>
  <tr>
    <th colspan="2">文件及美化工具</th>
  </tr>
  <tr>
    <td>文件</td>
    <td>Microsoft Word、Excel</td>
  </tr>
  <tr>
    <td>圖表</td>
    <td>Diagram.net、Canva</td>
  </tr>
  <tr>
    <td>簡報</td>
    <td>Microsoft PowerPoint、Canva</td>
  </tr>
</table>  
<table>
  <tr>
    <th colspan="2">專案管理及版本控制工具</th>
  </tr>
  <tr>
    <td>應用程式</td>
    <td>Fork</td>
  </tr>
  <tr>
    <td>版本控制</td>
    <td>Git</td>
  </tr>
</table> 

## 需求模型
### 使用者需求
- 功能性需求
<table>
  <tr>
    <th>項目</th>
    <th>說明</th>
  </tr>
  <tr>
    <td>會員登入</td>
    <td>使用者可用Google帳號進行登入。</td>
  </tr>
  <tr>
    <td>檢視會員資料</td>
    <td>使用者可查看他們的個人資訊</td>
  </tr>
  <tr>
    <td>修改會員資料</td>
    <td>使用者可修改他們的個人資訊</td>
  </tr>
  <tr>
    <td>生成食譜</td>
    <td>使用者可使用Banana營養師生成食譜</td>
  </tr>
  <tr>
    <td>檢視食譜</td>
    <td>使用者可查看他們用Banana營養師生成的食譜</td>
  </tr>
  <tr>
    <td>檢視收藏列表</td>
    <td>使用者可查看他們的收藏列表</td>
  </tr>
  <tr>
    <td>新增收藏</td>
    <td>使用者可以將喜歡的貼文加進收藏列表</td>
  </tr>
  <tr>
    <td>修改收藏列表</td>
    <td>使用者可以修改收藏列表中貼文的收藏列表</td>
  </tr>
  <tr>
    <td>新增體重紀錄</td>
    <td>使用者可新增體重紀錄</td>
  </tr>
  <tr>
    <td>發佈貼文</td>
    <td>使用者可以發佈貼文</td>
  </tr>
  <tr>
    <td>發佈生成食譜</td>
    <td>使用者可發佈他們用Banana營養師生成的食譜</td>
  </tr>
  <tr>
    <td>按讚及留言</td>
    <td>使用者可以對貼文按讚和留言</td>
  </tr>
</table> 

- 非功能性需求
<table>
  <tr>
    <th>項目</th>
    <th>說明</th>
  </tr>
  <tr>
    <td>易用性</td>
    <td>系統須提供易用的使用界面，讓使用者能有好的體驗。</td>
  </tr>
  <tr>
    <td>可維護性</td>
    <td>系統須具備良好的維護性，代碼應易於理解、修改和擴展。</td>
  </tr>
  <tr>
    <td>安全性</td>
    <td>系統須保護使用者的數據，防止未經授權的訪問和攻擊。</td>
  </tr>
</table>  

### 使用個案圖
## 結論及未來發展
