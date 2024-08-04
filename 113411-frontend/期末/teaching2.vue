<template>

  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>投資學習之AI應用</title>
  </head>

  <body>
      <header>
          <img src="../assets/1.png" alt="金融資訊網站標誌">
          <div class="separator"></div>
          <div class="header-text">
              <h1>投資學習之AI應用</h1>
              <h1>新手小學堂</h1>
          </div>
      </header>
      <main>
          <!-- 1. 股票入門必看基礎 -->
          <section id="intro" class="gray-section">
              <h2>一、股票入門必看基礎</h2>
              <div class="text-block1">
                  <h3>1.什麼是股票?</h3>
                  <p>股票是公司發行的股份，代表持有人擁有公司的一部分權益。當你購買公司的股票時，你實際上成為了該公司的部分所有者。</p>
              </div>
              <h3>2.股票入門基礎知識</h3>
              <div class="card-container">
                  <div class="card" id="code">
                      <p>股票代碼</p>
                      <div class="card-content">
                          <p>股票代碼（Stock Symbol），又稱股票代號，是用來標識特定公司的簡短字母或數字組合。每家上市公司的股票都有一個唯一的股票代碼，用於在證券交易所進行交易。</p>
                      </div>、
                  </div>
                  <div class="card" id="price">
                      <p>股票價格</p>
                      <div class="card-content">
                          <p>看盤時我們所看到的是股票單價，也就是每一股的價格。而股票的成交價通常是由市場的買方、賣方共同決定，但不像房屋交易那樣會有房屋仲介媒合，股票通常是由證券交易所的電腦系統進行撮合。
                          </p>
                      </div>
                  </div>
                  <div class="card" id="time">
                      <p>股票交易時間</p>
                      <div class="card-content">
                          <p>股票市場並非24小時都開放，通常會有指定開放交易的時間。以台灣為例，股票市場的交易時間為每週一至週五的9:00～13:30，盤後定價交易時間為14:00～14:30，而零股盤後交易時間為13:40～14:30。
                          </p>
                      </div>
                  </div>
              </div>
          </section>

          <!-- 2. 認識台灣股票市場 -->
          <section id="market" class="beige-section">
              <h2>二、認識台灣股票市場</h2>
              <div class="grid-container">
                  <div class="grid-item left" id="item1">
                      <h3>01 股票買賣單位</h3>
                      <p>● 張：台灣股票市場中，股票的基本買賣單位是一張，每張股票代表1000股。</p>
                      <p>● 零股：如果投資者希望買賣少於一張（即1000股）的股票，可以通過零股交易進行，選擇購買1～999股。零股交易通常在盤後進行。</p>
                  </div>
                  <div class="grid-item right" id="item2">
                      <h3>02 上市、上櫃、興櫃</h3>
                      <p>世界各國的股票市場大致分為上市、上櫃、興櫃三種，台灣股市也不例外。最簡單區分上市、上櫃、興櫃的方法是觀察「最低實收資本額」，興櫃公司若高於門檻就能往上櫃前進，以此類推。</p>
                  </div>
                  <div class="grid-item left" id="item3">
                      <h3>03 三大法人</h3>
                      <p>在台灣股票市場，三大法人指的是市場上主要的機構投資者，分別是外資、投信和自營商，這些法人對股市的影響力非常大。</p>
                  </div>
              </div>
          </section>

          <!-- 3. 股票損益與費用 -->
          <section id="profit-loss" class="gray-section">
              <h2>三、股票損益與費用</h2>
              <div class=".profit-container">
                  <h3>投資股票獲利最主要為2種</h3>
                  <div class="profit-types">
                      <div class="profit-type">
                          <h3>股票賺價差</h3>
                          <p>股價上漲並賺取股票價差</p>
                      </div>
                      <div class="profit-type">
                          <h3>股息</h3>
                          <p>公司賺錢時，把獲利的一部分分給股東</p>
                      </div>
                  </div>
              </div>

              <div class=".profit-container">
                  <h3>潛在的股票交易成本最主要為3種</h3>
                  <div class="cost-types">
                      <div class="cost-type">
                          <h3>手續費</h3>
                          <p>股票交易手續費計算為購買金額的0.1425%，而股票成交手續費未滿20元會按20元計收，並且當股票買進時會收一次手續費，而股票賣出時也會收一次。</p>
                      </div>
                      <div class="cost-type">
                          <h3>交易稅</h3>
                          <p>要賣出台股時，除了手續費之外，還需要付0.30%的交易稅（僅在賣出時才會需要付）。</p>
                      </div>
                      <div class="cost-type">
                          <h3>股利所得稅</h3>
                          <p>買公司股票後，如果手上的股票有參與除權息並收到現金股利，隔年就會被課稅。台灣現行法規有兩種計算方式：(1) 股利所合併計稅 (2) 股利單獨計稅。</p>
                      </div>
                  </div>
              </div>
          </section>

          <!-- 4. 股票類型 -->
          <section id="types" class="beige-section">
              <div class="types-container">
                  <h2>四、股票類型</h2>
                  <div class="text-block">
                      <h3>01 股票市值</h3>
                      <p4> ● 大盤股：市值較大的公司股票，如台積電、鴻海。</p4>
                      <p4> ● 中小盤股：市值較小的公司股票，通常波動性較大，但成長潛力較高。</p4>
                  </div>
                  <hr>
                  <div class="text-block">
                      <h3>02 產業類別</h3>
                      <p4>可以參考《產業價值鏈資訊平台》，是由「台灣證券交易所」及「櫃檯買賣中心」所建立的免費資料庫，平台統計全台發行合法股票的企業，並將產業分為30個大分類，旗下還有子分類，方便大家快速了解產業結構，適合股票市場入門研究。投資者了解市場的不同部分，並分散投資風險，選擇適合的產業進行投資，能夠根據經濟周期和市場趨勢做出更明智的決策。
                      </p4>
                  </div>
                  <hr>
                  <div class="text-block">
                      <h3>03 股票特性</h3>
                      <p4> ● 藍籌股：大型、穩定、具良好業績記錄的公司股票，如台積電。</p4>
                      <p4> ● 成長股：具有高成長潛力的公司股票，通常來自快速增長的行業，如科技股。</p4>
                      <p4> ● 價值股：目前被市場低估，但基本面良好的公司股票，適合長期投資。</p4>
                      <p4> ● 週期股：業績和股價隨經濟周期波動的公司股票，如鋼鐵、化工類股。</p4>
                  </div>
              </div>
          </section>

          <!-- 5. 股票走勢如何看 -->
          <section id="trends" class="gray-section">
              <h2>五、股票走勢如何看</h2>
              <table class="trends-table">
                  <tr>
                      <td>
                          <div class="trend-item">
                              <h3>分析技術指標</h3>
                              <p>金融分析技術指標是利用數據計算、圖表顯示金融市場趨勢和交易信號的工具。</p>
                              <button onclick="toggleText(this)">Read more</button>
                              <div class="more-text">
                                  <li>移動平均線（MA）：短期、中期和長期均線的走勢和交叉情況，可以判斷趨勢的強弱和方向。</li>
                                  <li>黃金交叉：短期均線向上穿越長期均線，通常視為買入信號。</li>
                                  <li>死亡交叉：短期均線向下穿越長期均線，通常視為賣出信號。</li>
                                  <li>相對強弱指數（RSI）：當日RSI值可以判斷股票是否處於超買或超賣狀態。</li>
                                  <li>RSI > 70：通常視為超買，可能會出現回調。</li>
                                  <li>{{rsiText}}</li>
                                         
                              </div>
                          </div>
                      </td>
                      <td>
                          <div class="trend-item">
                              <h3>開盤價/收盤價</h3>
                              <li>開盤價：觀察開盤價相對於前一日收盤價的變化，可以了解市場情緒。</li>
                              <li>收盤價：當日收盤價相對於開盤價和當日最高、最低價的位置，幫助判斷當日趨勢。</li>
                          </div>
                      </td>
                      <td>
                          <div class="trend-item">
                              <h3>市場情緒</h3>
                              <li>市場情緒：觀察市場的整體情緒，包括大盤走勢和其他個股的表現。</li>
                              <li>消息面：當日是否有影響市場的重大消息，如公司公告、宏觀經濟數據、國際事件等。</li>
                          </div>
                      </td>
                  </tr>
                  <tr>
                      <td>
                          <div class="trend-item">
                              <h3>內外盤比例</h3>
                              <p>內外盤比就是在五檔報價上面，一條綠色及紅色的比。</p>
                              <button onclick="toggleText(this)">Read more</button>
                              <div class="more-text">
                                  <li>成交在外盤>成交在內盤：比較多人用外盤（較貴）的價格成交，代表多數人都搶著買這支股票。</li>
                                  <li>成交在內盤>成交在外盤：比較多人用內盤（較便宜）的價格成交，代表多數人都搶著賣掉這支股票。</li>
                              </div>
                          </div>
                      </td>
                      <td>
                          <div class="trend-item">
                              <h3>分析K線圖</h3>
                              <p>當日K線的形態可以揭示當日的市場動向。</p>
                              <button onclick="toggleText(this)">Read more</button>
                              <div class="more-text">
                                  <li>紅K線（陽線）：表示收盤價高於開盤價，當日價格上漲。</li>
                                  <li>綠K線（陰線）：表示收盤價低於開盤價，當日價格下跌。</li>
                                  <li>上影線和下影線：影線的長短反映當日價格波動幅度和買賣力量的對比。</li>
                              </div>
                          </div>
                      </td>
                      <td>
                          <div class="trend-item">
                              <h3>成交量</h3>
                              <p>當日成交量相對於前幾日的變化，可以判斷市場參與的積極性。</p>
                              <button onclick="toggleText(this)">Read more</button>
                              <div class="more-text">
                                  <li>放量上漲：價格上漲伴隨成交量增加，通常表示市場看好後市。</li>
                                  <li>放量下跌：價格下跌伴隨成交量增加，通常表示市場看淡後市。</li>
                              </div>
                          </div>
                      </td>
                  </tr>
              </table>
          </section>

          <!-- 6. 新手的3種投資策略 -->
          <section id="strategies" class="beige-section strategies-section">
              <h2>六、新手的3種投資策略</h2>
              <div class="strategy">
                  <div class="strategy-header">投資入門策略1：股票分散風險</div>
                  <div class="strategy-content">
                      「雞蛋不要放在同一個籃子裡」將資金分散投資於多種股票和資產，以降低單一股票或行業波動對投資組合的影響。此種策略是股票投資的基礎策略，通過投資不同的行業、市值、地區，結合成長股和價值股，並定期檢視和調整投資組合，能夠有效降低風險，獲得穩定的投資回報。
                  </div>
              </div>
              <div class="strategy">
                  <div class="strategy-header">投資入門策略2：定期定額投資</div>
                  <div class="strategy-content">
                      定期定額投資策略是一種簡單且有效的投資方法，適合新手投資者。通過定期投入固定金額，平滑市場波動，降低平均購買成本，並減少情緒干擾，實現穩定的長期回報。選擇適合的投資標的，保持紀律和耐心，是成功實施這一策略的關鍵。
                  </div>
              </div>
              <div class="strategy">
                  <div class="strategy-header">投資入門策略3：買入並持有策略</div>
                  <div class="strategy-content">
                      買入並持有策略是一種簡單且有效的長期投資方法，適合那些希望通過穩定的股息和資本增值來實現財務目標的投資者。選擇基本面良好且具有長期成長潛力的公司，並在市場波動時保持耐心，這一策略能夠幫助投資者避免短期市場波動的影響，實現穩定的投資回報。
                  </div>
              </div>
          </section>

          <!-- 7. 股票名詞懶人包 -->
          <section id="glossary" class="gray-section">
              <h2>七、股票名詞懶人包</h2>
              <div class="tab">
                  <button class="tablinks"@click="openTab(event, 'basic')"  id="defaultOpen"><strong>基本術語</strong></button>
                  <button class="tablinks" @click="openTab(event, 'transaction')"><strong>交易相關術語</strong></button>
                  <button class="tablinks" @click="openTab(event, 'mar')"><strong>市場指標</strong></button>
                  <button class="tablinks" @click="openTab(event, 'technical')"><strong>技術分析術語</strong></button>
                  <button class="tablinks" @click="openTab(event, 'common')"><strong>其他常見術語</strong></button>
                  <button class="tablinks" @click="openTab(event, 'chinese')"><strong>中文特有術語</strong></button>
              </div>

              <div id="basic" class="tabcontent">
                  <ul>
                      <li><strong>股票（Stock）：</strong>代表公司部分所有權的證券。</li>
                      <li><strong>股東（Shareholder）：</strong>擁有公司股票的個人或實體。</li>
                      <li><strong>市值（Market Capitalization）：</strong>公司所有流通股票的總價值，計算公式為股票價格乘以總股數。</li>
                      <li><strong>股息（Dividend）：</strong>公司盈利的一部分分配給股東的現金或股票。</li>
                  </ul>
              </div>

              <div id="transaction" class="tabcontent">
                  <ul>
                      <li><strong>買入（Buy）：</strong>購買股票。</li>
                      <li><strong>賣出（Sell）：</strong>賣出股票。</li>
                      <li><strong>持有（Hold）：</strong>保留現有的股票，不買也不賣。</li>
                      <li><strong>買賣價差（Market Order）：</strong>按當前市場價格立即買入或賣出的訂單。</li>
                  </ul>
              </div>

              <div id="mar" class="tabcontent">
                  <ul>
                      <li><strong>道瓊斯工業平均指數（DJIA）：</strong>包含30家大型美國公司股票價格的加權指數。</li>
                      <li><strong>標普500指數（S&P 500 Index）：</strong>包含500家大型美國公司的股票指數。</li>
                      <li><strong>納斯達克綜合指數（Nasdaq Composite Index）：</strong>主要由科技公司組成的指數。</li>
                  </ul>
              </div>


              <div id="technical" class="tabcontent">
                  <ul>
                      <li><strong>支撐位（Support Level）：</strong>股票價格下跌時預期會遇到支撐的價格水平。</li>
                      <li><strong>阻力位（Resistance Level）：</strong>股票價格上漲時預期會遇到阻力的價格水平。</li>
                      <li><strong>移動平均線（Moving Average, MA）：</strong>某段時間內股票價格的平均值，用來平滑價格波動。</li>
                      <li><strong>成交量（Volume）：</strong>在一定時間內交易的股票數量。</li>
                  </ul>
              </div>

              <div id="common" class="tabcontent">
                  <ul>
                      <li><strong>多頭（Bull）：</strong>對市場前景持樂觀態度並預期價格上漲的投資者。</li>
                      <li><strong>空頭（Bear）：</strong>對市場前景持悲觀態度並預期價格下跌的投資者。</li>
                      <li><strong>IPO（Initial Public Offering）：</strong>公司首次公開發行股票。</li>
                      <li><strong>市盈率（P/E Ratio）：</strong>股票價格與每股收益的比率，用來評估股票的估值水平。</li>
                      <li><strong>分紅（Dividend）：</strong>公司將部分利潤分配給股東的現金或股票。</li>
                  </ul>
              </div>

              <div id="chinese" class="tabcontent">
                  <ul>
                      <li><strong>韭菜：</strong>菜鳥散戶。</li>
                      <li><strong>割韭菜：</strong>機構投機人、大戶藉由拉抬操作股價，等到股價到了高點後再一次倒貨給散戶。</li>
                      <li><strong>大戶：</strong>擁有資金量龐大的投資人。</li>
                      <li><strong>大盤：</strong>台股的整體表現，通常指的是台灣加權指數。</li>
                      <li><strong>套牢：</strong>投資人在購買股票後，股價不漲反跌，若以現價賣出就會直接實現虧損，因此只能繼續持有股票，希望未來股價能夠回升。</li>
                      <li><strong>接刀：</strong>股價大幅下跌時，投資人進場撿便宜的股票，但卻不幸撿到不斷下跌（甚至下市）的股票。</li>
                      <li><strong>抄底：</strong>股價大幅下跌時，投資人搶進場撿便宜的股票，並成功以低價購入股票。</li>
                      <li><strong>跳水：</strong>股價驟跌。</li>
                      <li><strong>畢業：</strong>全身的資金都賠光光，無法再加入股市。</li>
                      <li><strong>牛皮：</strong>股性堅強，不易受波動影響。</li>
                      <li><strong>法會：</strong>釋出許多利多消息，造成股市大跌的法說會。</li>
                      <li><strong>抬轎：</strong>當股價上漲後，一些投資人跟著買進湊熱鬧，這時後面進場的人就等於幫先前已佈局的人「抬高」股價。</li>
                      <li><strong>砍在阿呆谷：</strong>代表股價下跌後停損，但停損後股價又反彈。</li>
                      <li><strong>凹單：</strong>跌破原先設定的出場價，但仍不願賣掉停損。</li>
                      <li><strong>資金盤：</strong>即「龐氏騙局（Ponzi Scheme）、金字塔騙局」，以高額報酬吸引投資人，以後加入的本金支付先加入的利息，最後捲款而逃。</li>
                      <li><strong>牛市：</strong>股價呈現上漲趨勢。</li>
                      <li><strong>熊市：</strong>股價呈現下跌趨勢。</li>
                      <li><strong>軋空（Short Squeeze）：</strong>做空的人看錯行情，被強迫平倉或買進股票回補。如果遇到大批做空的人回補股票，會造成股價暴漲。</li>
                      <li><strong>破底：</strong>股價下跌到某個價位，賣方力量勝過買方支撐力量。</li>
                      <li><strong>斷頭：</strong>融資買股票，看錯不停損，但又繳不出保證金，因此被券商出清股票。</li>
                      <li><strong>跳空：</strong>連續兩天的K線價格不重疊，若是向上跳空，表示買進力道強勁。</li>
                      <li><strong>當沖（Day Trading）：</strong>在同一個交易日當中，買進賣出同樣數量的股票，並在當日結清部位。</li>
                      <li><strong>漲停、跌停：</strong>表示股價當天達到最大的上漲、下跌幅度限制，以台股來說為正負10%。</li>
                      <li><strong>飆股：</strong>股性活潑，連續跳空漲停的標的。</li>
                      <li><strong>景氣循環股：</strong>公司營收和景氣循環有密切相關的產業類股，例如鋼鐵、航運、石化。</li>
                      <li><strong>權值股：</strong>市值佔市場（台股加權指數）比重大的股票。</li>
                      <li><strong>雞蛋水餃股/銅板股：</strong>泛指股價低於10元（1萬元）的便宜股票。</li>
                      <li><strong>VIX（Volatility Index）：</strong>由芝加哥選擇權交易所所推出的市場未來波動指數，通常用於檢視市場投資人的恐慌情緒。</li>
                  </ul>
              </div>
          </section>
      </main>
  </body>

  <!DOCTYPE html>
  <html lang="zh-Hant">

  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>投資學習之AI應用</title>
      <link rel="stylesheet" href="styles.css">
  </head>

  <body>
      <header>
          <img src="S__3579960_0-removebg-preview.png" alt="金融資訊網站標誌">
          <div class="separator"></div>
          <div class="header-text">
              <h1>投資學習之AI應用</h1>
              <h1>新手小學堂</h1>
          </div>
      </header>
      <main>
          <!-- 1. 股票入門必看基礎 -->
          <section id="intro" class="gray-section">
              <h2>一、股票入門必看基礎</h2>
              <div class="text-block1">
                  <h3>1.什麼是股票?</h3>
                  <p>股票是公司發行的股份，代表持有人擁有公司的一部分權益。當你購買公司的股票時，你實際上成為了該公司的部分所有者。</p>
              </div>
              <h3>2.股票入門基礎知識</h3>
              <div class="card-container">
                  <div class="card" id="code">
                      <p>股票代碼</p>
                      <div class="card-content">
                          <p>股票代碼（Stock Symbol），又稱股票代號，是用來標識特定公司的簡短字母或數字組合。每家上市公司的股票都有一個唯一的股票代碼，用於在證券交易所進行交易。</p>
                      </div>
                  </div>
                  <div class="card" id="price">
                      <p>股票價格</p>
                      <div class="card-content">
                          <p>看盤時我們所看到的是股票單價，也就是每一股的價格。而股票的成交價通常是由市場的買方、賣方共同決定，但不像房屋交易那樣會有房屋仲介媒合，股票通常是由證券交易所的電腦系統進行撮合。
                          </p>
                      </div>
                  </div>
                  <div class="card" id="time">
                      <p>股票交易時間</p>
                      <div class="card-content">
                          <p>股票市場並非24小時都開放，通常會有指定開放交易的時間。以台灣為例，股票市場的交易時間為每週一至週五的9:00～13:30，盤後定價交易時間為14:00～14:30，而零股盤後交易時間為13:40～14:30。
                          </p>
                      </div>
                  </div>
              </div>
          </section>

          <!-- 2. 認識台灣股票市場 -->
          <section id="market" class="beige-section">
              <h2>二、認識台灣股票市場</h2>
              <div class="grid-container">
                  <div class="grid-item left" id="item1">
                      <h3>01 股票買賣單位</h3>
                      <p>● 張：台灣股票市場中，股票的基本買賣單位是一張，每張股票代表1000股。</p>
                      <p>● 零股：如果投資者希望買賣少於一張（即1000股）的股票，可以通過零股交易進行，選擇購買1～999股。零股交易通常在盤後進行。</p>
                  </div>
                  <div class="grid-item right" id="item2">
                      <h3>02 上市、上櫃、興櫃</h3>
                      <p>世界各國的股票市場大致分為上市、上櫃、興櫃三種，台灣股市也不例外。最簡單區分上市、上櫃、興櫃的方法是觀察「最低實收資本額」，興櫃公司若高於門檻就能往上櫃前進，以此類推。</p>
                  </div>
                  <div class="grid-item left" id="item3">
                      <h3>03 三大法人</h3>
                      <p>在台灣股票市場，三大法人指的是市場上主要的機構投資者，分別是外資、投信和自營商，這些法人對股市的影響力非常大。</p>
                  </div>
              </div>
          </section>

          <!-- 3. 股票損益與費用 -->
          <section id="profit-loss" class="gray-section">
              <h2>三、股票損益與費用</h2>
              <div class="profit-container">
                  <h3>投資股票獲利最主要為2種</h3>
                  <div class="profit-types">
                      <div class="profit-type">
                          <h3>股票賺價差</h3>
                          <p>股價上漲並賺取股票價差</p>
                      </div>
                      <div class="profit-type">
                          <h3>股息</h3>
                          <p>公司賺錢時，把獲利的一部分分給股東</p>
                      </div>
                  </div>
              </div>

              <div class="profit-container">
                  <h3>潛在的股票交易成本最主要為3種</h3>
                  <div class="cost-types">
                      <div class="cost-type">
                          <h3>手續費</h3>
                          <p>股票交易手續費計算為購買金額的0.1425%，而股票成交手續費未滿20元會按20元計收，並且當股票買進時會收一次手續費，而股票賣出時也會收一次。</p>
                      </div>
                      <div class="cost-type">
                          <h3>交易稅</h3>
                          <p>要賣出台股時，除了手續費之外，還需要付0.30%的交易稅（僅在賣出時才會需要付）。</p>
                      </div>
                      <div class="cost-type">
                          <h3>股利所得稅</h3>
                          <p>買公司股票後，如果手上的股票有參與除權息並收到現金股利，隔年就會被課稅。台灣現行法規有兩種計算方式：(1) 股利所合併計稅 (2) 股利單獨計稅。</p>
                      </div>
                  </div>
              </div>
          </section>

          <!-- 4. 股票類型 -->
          <section id="types" class="beige-section">
              <div class="types-container">
                  <h2>四、股票類型</h2>
                  <div class="text-block">
                      <h3>01 股票市值</h3>
                      <p>● 大盤股：市值較大的公司股票，如台積電、鴻海。</p>
                      <p>● 中小盤股：市值較小的公司股票，通常波動性較大，但成長潛力較高。</p>
                  </div>
                  <hr>
                  <div class="text-block">
                      <h3>02 產業類別</h3>
                      <p>可以參考《產業價值鏈資訊平台》，是由「台灣證券交易所」及「櫃檯買賣中心」所建立的免費資料庫，平台統計全台發行合法股票的企業，並將產業分為30個大分類，旗下還有子分類，方便大家快速了解產業結構，適合股票市場入門研究。投資者了解市場的不同部分，並分散投資風險，選擇適合的產業進行投資，能夠根據經濟周期和市場趨勢做出更明智的決策。
                      </p>
                  </div>
                  <hr>
                  <div class="text-block">
                      <h3>03 股票特性</h3>
                      <p>● 藍籌股：大型、穩定、具良好業績記錄的公司股票，如台積電。</p>
                      <p>● 成長股：具有高成長潛力的公司股票，通常來自快速增長的行業，如科技股。</p>
                      <p>● 價值股：目前被市場低估，但基本面良好的公司股票，適合長期投資。</p>
                      <p>● 週期股：業績和股價隨經濟周期波動的公司股票，如鋼鐵、化工類股。</p>
                  </div>
              </div>
          </section>

          <!-- 5. 股票走勢如何看 -->
          <section id="trends" class="gray-section">
              <h2>五、股票走勢如何看</h2>
              <div class="trend-container">
                  <h3>01 股票走勢圖</h3>
                  <p>可以觀察股票價格隨時間變動的圖表，有助於了解股票的歷史表現和未來趨勢。</p>
                  <p>● <b>K線圖：</b> K線圖，又稱蠟燭圖，顯示股票每日的開盤價、收盤價、最高價和最低價。K線圖是技術分析中最常用的圖表之一。</p>
                  <p>● <b>均線圖：</b> 均線圖顯示一段時間內的平均價格變化，有助於識別股票的趨勢。</p>
              </div>
              <div class="trend-container">
                  <h3>02 股價指標</h3>
                  <p>● <b>成交量：</b> 成交量是指某段時間內交易的股票數量，成交量的變化可以反映市場的熱度和趨勢。</p>
                  <p>● <b>市盈率：</b> 市盈率是衡量股票價值的一個重要指標，計算方法是股票價格除以每股收益（EPS）。</p>
                  <p>● <b>股價淨值比：</b> 股價淨值比是股票價格與每股淨資產的比率，是衡量股票價值的一個常用指標。</p>
              </div>
          </section>

          <!-- 6. 如何挑選潛力股 -->
          <section id="potential" class="beige-section">
              <h2>六、如何挑選潛力股</h2>
              <div class="potential-container">
                  <div class="text-block">
                      <h3>01 基本面分析</h3>
                      <p>基本面分析是透過分析公司的財務狀況、行業趨勢、經營管理等因素來評估股票價值的方法。</p>
                      <p>● <b>財務報表：</b> 了解公司的資產負債表、損益表和現金流量表，可以評估公司的財務狀況和盈利能力。</p>
                      <p>● <b>行業趨勢：</b> 分析公司的行業地位和市場競爭力，了解行業的發展趨勢和未來潛力。</p>
                      <p>● <b>經營管理：</b> 了解公司的經營策略、管理團隊和公司治理，評估公司的未來發展潛力。</p>
                  </div>
                  <div class="text-block">
                      <h3>02 技術面分析</h3>
                      <p>技術面分析是通過分析股票價格和成交量的歷史數據，預測股票價格未來走勢的方法。</p>
                      <p>● <b>趨勢分析：</b> 觀察股票價格的趨勢，識別上升趨勢、下降趨勢和橫盤整理趨勢。</p>
                      <p>● <b>技術指標：</b> 使用各種技術指標，如移動平均線、相對強弱指數（RSI）、隨機指標等，來輔助分析股票價格走勢。</p>
                      <p>● <b>K線形態：</b> 觀察K線圖的形態，如頭肩頂、雙底、旗形等，預測股票價格的變化。</p>
                  </div>
              </div>
          </section>

          <!-- 7. 如何利用AI技術提高投資效率 -->
          <section id="ai" class="gray-section">
              <h2>七、如何利用AI技術提高投資效率</h2>
              <div class="ai-container">
                  <div class="ai-text">
                      <p>AI技術在投資領域的應用越來越廣泛，可以幫助投資者提高投資效率和決策質量。</p>
                      <h3>01 自動化交易</h3>
                      <p>利用AI技術，可以實現自動化交易，根據預設的交易策略自動執行交易，減少人為干預和情緒影響。</p>
                      <h3>02 大數據分析</h3>
                      <p>AI技術可以快速處理和分析大量數據，從中提取有價值的信息，幫助投資者做出更明智的決策。</p>
                      <h3>03 預測模型</h3>
                      <p>通過機器學習和數據挖掘技術，AI可以建立預測模型，預測股票價格的變化趨勢，提高投資成功率。</p>
                  </div>
              </div>
          </section>
      </main>

      <footer>
          <p>© 2023 投資學習之AI應用. 版權所有.</p>
      </footer>
  </body>

  </html>
</template>

<script>
export default {
  name: 'TeachingForm',
  data() {
      return {
          rsiText: 'RSI < 30：通常視為超賣,可能會出現反彈。',
          isTextVisible: false,
          activeTab: null
      };
  },
  mounted() {
      this.addEventListeners();
      this.$nextTick(() => {
          document.getElementById("defaultOpen").click();
      });
  },
  methods: {
      toggleText() {
          this.isTextVisible = !this.isTextVisible;
      },
      openTab(tabName) {
          this.activeTab = tabName;
      },
      addEventListeners() {
          document.addEventListener("DOMContentLoaded", () => {
              this.addFadeInEffect();
              this.addHoverEffect();
              this.addCollapsibleBehavior();
              this.addStrategyTableFadeOut();
              this.addSmoothScrolling();
              this.addSlideInEffect();
          });

          window.addEventListener('scroll', () => {
              var sections = document.querySelectorAll('section');
              sections.forEach(function (section) {
                  var rect = section.getBoundingClientRect();
                  if (rect.top < window.innerHeight && rect.bottom >= 0) {
                      section.classList.remove('fade-out');
                  } else {
                      section.classList.add('fade-out');
                  }
              });
          });
      },
      addFadeInEffect() {
          document.querySelectorAll('.text-block').forEach(function (el) {
              el.style.opacity = 0;
              setTimeout(function () {
                  el.style.opacity = 1;
              }, 500);
          });
          // Add hover effect to cards
          document.querySelectorAll('.card').forEach(function (el) {
              el.addEventListener('mouseover', function () {
                  this.style.transform = 'scale(1.1)';
              });
              el.addEventListener('mouseout', function () {
                  this.style.transform = 'scale(1)';
              });




              // Add collapsible behavior
              document.querySelectorAll('.collapsible').forEach(function (el) {
                  el.addEventListener('click', function () {
                      this.classList.toggle('active');
                      let content = this.nextElementSibling;
                      if (content.style.maxHeight) {
                          content.style.maxHeight = null;
                      } else {
                          content.style.maxHeight = content.scrollHeight + "px";
                      }
                  });
              });



              // Add fade-out effect on scroll for strategy table
              const strategyTable = document.querySelector('#strategies .table');
              window.addEventListener('scroll', function () {
                  if (window.scrollY + window.innerHeight >= strategyTable.offsetTop) {
                      strategyTable.style.opacity = 0;
                  } else {
                      strategyTable.style.opacity = 1;
                  }
              });


              // Add scroll effect for smooth scrolling
              document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                  anchor.addEventListener('click', function (e) {
                      e.preventDefault();
                      document.querySelector(this.getAttribute('href')).scrollIntoView({
                          behavior: 'smooth'
                      });
                  });
              });

              // Add slide-in effect for sections
              const sections = document.querySelectorAll('section');
              const options = {
                  threshold: 0.1
              };
              const observer = new IntersectionObserver(function (entries, observer) {
                  entries.forEach(entry => {
                      if (!entry.isIntersecting) {
                          return;
                      }
                      entry.target.classList.add('slide-in');
                      observer.unobserve(entry.target);
                  });
              }, options);
              sections.forEach(section => {
                  observer.observe(section);
              });
          });
         
          window.addEventListener('scroll', function () {
              var sections = document.querySelectorAll('section');
              sections.forEach(function (section) {
                  var rect = section.getBoundingClientRect();
                  if (rect.top < window.innerHeight && rect.bottom >= 0) {
                      section.classList.remove('fade-out');
                  } else {
                      section.classList.add('fade-out');
                  }
              });
          });

         

          document.getElementById("defaultOpen").click();
      }
  }
}
</script>

<style>
header {
  display: flex;
  align-items: center;
  justify-content: center;
  /* 水平方向居中 */
  text-align: center;
  /* 文字居中 */
}

header img {
  margin-right: 3px;
  /* 調整間距 */
}

.header-text {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.separator {
  width: 3px;
  height: 75px;
  /* 調整高度 */
  background-color: #f8f9fa;
  /* 調整顏色 */
  margin-left: 10px;
  /* 調整間距 */
  margin-right: 10px;
  /* 調整間距 */
}

body {
  font-family: Arial, sans-serif;
  background-color: #f8f9fa;
  color: #333;
  text-align: center;
  margin: 0;
  padding: 0;
  font-weight: bold;
  /* 設置全局文字為粗體 */
}

header {
  background-color: #57614E;
  color: #fff;
  padding: 1em 0;
}

h1 {
  margin: 0;
}

main {
  padding: 0;
  /* 移除main元素的內邊距 */
}

.gray-section {
  background-color: #bdbdbd;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.beige-section {
  background-color: #E9E9E9;
  padding: 2em;
  margin: 0;
  /* 移除外邊距 */
}

section {
  opacity: 0;
  transform: translateY(50px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

section.slide-in {
  opacity: 1;
  transform: translateY(0);
}

h2 {
  padding: 1em;
  margin: 0;
  /* 移除外邊距 */
  font-size: 50px
}

h3 {
  font-size: 32px;
  margin: 1em 0;
}

p {
  font-size: 24px;
}

li {
  font-size: 20px;
  /* 設定字體大小為 20 像素 */
}

p4 {
  display: flex;
  align-items: center;
  /* 垂直置中 */
  text-align: left;
  /* 左對齊 */
  font-size: 24px;
}

.text-block {
  margin: 1em 0;
  padding: 1em;
  text-align: left;
  /* 文字靠左對齊 */
  display: flex;
  /* 使用 flex 排版 */
  flex-direction: column;
  /* 垂直排列 */
  justify-content: center;
  /* 垂直置中 */
  align-items: center;
  /* 水平置中 */
  height: 200px;
  /* 根據需要調整 */
  transition: transform 0.3s, background-color 0.3s;
}

.card-container {
  display: flex;
  justify-content: space-between;
  margin: 0 auto;
  /* 移除上下外邊距 */
  padding: 0;
  /* 確保沒有內邊距 */
  width: 70%;
  /* 設置卡片寬度為30% */
}

.card {
  background-color: #fff;
  /* 白色背景 */
  color: #333;
  /* 深灰色文字 */
  padding: 1em;
  /* 減少內邊距 */
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s;
  border: 2px solid #333;
  /* 框線 */
  width: 30%;
  /* 設置卡片寬度為30% */
  margin: 0 0.5em;
  /* 左右外邊距確保卡片之間的間隔 */
}

.card-content {
  margin-top: 1em;
  text-align: left;
  border-top: 1px solid #333;
  /* 框線 */
  padding-top: 1em;
}

.text-block1 {
  margin: 1em 0;
  padding: 1em;
  transition: transform 0.3s, background-color 0.3s;
}

.text-block {
  margin: 1em 0;
  padding: 1em;
  text-align: left;
  align-items: center;
  /* 垂直置中 */
  transition: transform 0.3s, background-color 0.3s;
}

.text-block h4 {
  margin: 0;
  width: 80%;
  /* 調整寬度，使其不會撐滿整個容器 */
  text-align: left;
  /* 確保文字靠左對齊 */
}

.text-block:hover {
  transform: scale(1.05);
  background-color: #6d6d6a;
  /* 懸停時的背景色 */
}

.text-block.left {
  text-align: left;
}

.text-block.right {
  text-align: right;
}

.half {
  width: 45%;
  display: inline-block;
  vertical-align: top;
}

.table {
  display: flex;
  flex-wrap: wrap;
}

.cell {
  flex: 1 0 30%;
  margin: 1em;
  padding: 1em;
  transition: opacity 1s;
}

.cell.black {
  background-color: #333;
  color: #fff;
}

.cell.beige {
  background-color: #6d6d6a;
  color: #333;
}

hr {
  margin: 2em 0;
}

.collapsible {
  cursor: pointer;
  background-color: #ccc;
  transition: height 0.3s, padding 0.3s;
}

.collapsible.active {
  height: auto;
  padding: 2em;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Hidden content for collapsible */
.content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
  padding: 0 18px;
}

.grid-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: repeat(3, auto);
  gap: 2em;
  justify-items: start;
  align-items: start;
  padding: 2em;
}

.grid-item {
  background-color: #E9E9E9;
  /* 杏色背景 */
  padding: 1em;
  text-align: left;
}

.grid-item#item1 {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
}

.grid-item#item2 {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
}

.grid-item#item3 {
  grid-column: 1 / 2;
  grid-row: 3 / 4;
}

.profit-types,
.cost-types {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.profit-type,
.cost-type {
  background-color: #666;
  color: #fff;
  margin: 0 10px;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
}

.profit-type:hover,
.cost-type:hover {
  transform: scale(1.05);
  background-color: #444;
}

.profit-container {
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.trends-table {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  border-collapse: collapse;
}

.trends-table td {
  text-align: center;
  padding: 20px;
  border: 1px solid #ccc;
}

.trend-item {
  position: relative;
  padding: 20px;
}

.more-text {
  display: none;
  text-align: left;
  margin-top: 10px;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.strategies-section {
  padding: 20px;
  background-color: #333;
  color: #fff;
}

.strategy {
  margin: 20px 0;
  padding: 20px;
  background-color: #444;
  border-radius: 8px;
  transition: transform 0.3s;
}

.strategy:hover {
  transform: scale(1.05);
}

.strategy-header {
  font-size: 32px;
  margin-bottom: 10px;
}

.strategy-content {
  font-size: 24px;
  text-align: left;
}

/* Styles for the tabs */
.tab {
  overflow: hidden;
  border-bottom: 1px solid #ccc;
  background-color: #f1f1f1;
  display: flex;
  justify-content: space-between;
  font-size: 24px;
  /* 字體大小 */
  font-family: Arial, sans-serif;
  /* 字體字形 */
  margin: 5px 0;
}

.tab button {
  background-color: inherit;
  flex: 1;
  /* Flex property to make buttons take equal space */
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
  font-size: 20px;
}

.tab button:hover {
  background-color: #ddd;
}

.tab button.active {
  background-color: #ccc;
}

.tabcontent {
  display: none;
  padding: 6px 12px;
  border-top: none;
  text-align: left;
}
</style>