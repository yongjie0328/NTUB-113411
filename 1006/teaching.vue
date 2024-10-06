<template>
    <div>
      <header>
        <img src="@/assets/S__3579960_0-removebg-preview.png" alt="金融資訊網站標誌" class="logo" />        <div class="separator"></div>
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
            <p>
              股票是公司發行的股份，代表持有人擁有公司的一部分權益。當你購買公司的股票時，你實際上成為了該公司的部分所有者。
            </p>
          </div>
          <h3>2.股票入門基礎知識</h3>
          <div class="card-container">
            <div class="card" id="code">
              <p>股票代碼</p>
              <div class="card-content">
                <p>
                  股票代碼（Stock Symbol），又稱股票代號，是用來標識特定公司的簡短字母或數字組合。每家上市公司的股票都有一個唯一的股票代碼，用於在證券交易所進行交易。
                </p>
              </div>
            </div>
            <div class="card" id="price">
              <p>股票價格</p>
              <div class="card-content">
                <p>
                  看盤時我們所看到的是股票單價，也就是每一股的價格。而股票的成交價通常是由市場的買方、賣方共同決定，但不像房屋交易那樣會有房屋仲介媒合，股票通常是由證券交易所的電腦系統進行撮合。
                </p>
              </div>
            </div>
            <div class="card" id="time">
              <p>股票交易時間</p>
              <div class="card-content">
                <p>
                  股票市場並非24小時都開放，通常會有指定開放交易的時間。以台灣為例，股票市場的交易時間為每週一至週五的9:00～13:30，盤後定價交易時間為14:00～14:30，而零股盤後交易時間為13:40～14:30。
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
              <p>
                ● 張：台灣股票市場中，股票的基本買賣單位是一張，每張股票代表1000股。
              </p>
              <p>
                ● 零股：如果投資者希望買賣少於一張（即1000股）的股票，可以通過零股交易進行，選擇購買1～999股。零股交易通常在盤後進行。
              </p>
            </div>
            <div class="grid-item right" id="item2">
              <h3>02 上市、上櫃、興櫃</h3>
              <p>
                世界各國的股票市場大致分為上市、上櫃、興櫃三種，台灣股市也不例外。最簡單區分上市、上櫃、興櫃的方法是觀察「最低實收資本額」，興櫃公司若高於門檻就能往上櫃前進，以此類推。
              </p>
            </div>
            <div class="grid-item center" id="item3">
              <h3>03 三大法人</h3>
              <p>
                在台灣股票市場，三大法人指的是市場上主要的機構投資者，分別是外資、投信和自營商，這些法人對股市的影響力非常大。
              </p>
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
                <h4>股票賺價差</h4>
                <p>股價上漲並賺取股票價差</p>
              </div>
              <div class="profit-type">
                <h4>股息</h4>
                <p>公司賺錢時，把獲利的一部分分給股東</p>
              </div>
            </div>
          </div>
  
          <div class="profit-container">
            <h3>潛在的股票交易成本最主要為3種</h3>
            <div class="cost-types">
              <div class="cost-type">
                <h4>手續費</h4>
                <p>
                  股票交易手續費計算為購買金額的0.1425%，而股票成交手續費未滿20元會按20元計收，並且當股票買進時會收一次手續費，而股票賣出時也會收一次。
                </p>
              </div>
              <div class="cost-type">
                <h4>交易稅</h4>
                <p>
                  要賣出台股時，除了手續費之外，還需要付0.30%的交易稅（僅在賣出時才會需要付）。
                </p>
              </div>
              <div class="cost-type">
                <h4>股利所得稅</h4>
                <p>
                  買公司股票後，如果手上的股票有參與除權息並收到現金股利，隔年就會被課稅。台灣現行法規有兩種計算方式：(1) 股利所合併計稅 (2) 股利單獨計稅。
                </p>
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
              <div class="p4">
                ● 大盤股：市值較大的公司股票，如台積電、鴻海。
              </div>
              <div class="p4">
                ● 中小盤股：市值較小的公司股票，通常波動性較大，但成長潛力較高。
              </div>
            </div>
            <hr />
            <div class="text-block">
              <h3>02 產業類別</h3>
              <div class="p4">
                可以參考《產業價值鏈資訊平台》，是由「台灣證券交易所」及「櫃檯買賣中心」所建立的免費資料庫，平台統計全台發行合法股票的企業，並將產業分為30個大分類，旗下還有子分類，方便大家快速了解產業結構，適合股票市場入門研究。投資者了解市場的不同部分，並分散投資風險，選擇適合的產業進行投資，能夠根據經濟周期和市場趨勢做出更明智的決策。
            
            </div>
            </div>
            <hr />
            <div class="text-block">
              <h3>03 股票特性</h3>
              <div class="p4">
                ● 藍籌股：大型、穩定、具良好業績記錄的公司股票，如台積電。
              </div>
              <div class="p4">
                ● 成長股：具有高成長潛力的公司股票，通常來自快速增長的行業，如科技股。
              </div>
              <div class="p4">
                ● 價值股：目前被市場低估，但基本面良好的公司股票，適合長期投資。
              </div>
              <div class="p4">
                ● 週期股：業績和股價隨經濟周期波動的公司股票，如鋼鐵、化工類股。
              </div>
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
                  <button @click="toggleText($event)">Read more</button>
                  <div class="more-text">
                    <ul>
                      <li>
                        移動平均線（MA）：短期、中期和長期均線的走勢和交叉情況，可以判斷趨勢的強弱和方向。
                      </li>
                      <li>黃金交叉：短期均線向上穿越長期均線，通常視為買入信號。</li>
                      <li>死亡交叉：短期均線向下穿越長期均線，通常視為賣出信號。</li>
                      <li>
                        相對強弱指數（RSI）：當日RSI值可以判斷股票是否處於超買或超賣狀態。
                      </li>
                      <li>RSI &gt; 70：通常視為超買，可能會出現回調。</li>
                      <li>RSI &lt; 30：通常視為超賣，可能會出現反彈。</li>
                    </ul>
                  </div>
                </div>
              </td>
              <td>
                <div class="trend-item">
                  <h3>開盤價/收盤價</h3>
                  <ul>
                    <li>
                      開盤價：觀察開盤價相對於前一日收盤價的變化，可以了解市場情緒。
                    </li>
                    <li>
                      收盤價：當日收盤價相對於開盤價和當日最高、最低價的位置，幫助判斷當日趨勢。
                    </li>
                  </ul>
                </div>
              </td>
              <td>
                <div class="trend-item">
                  <h3>市場情緒</h3>
                  <ul>
                    <li>
                      市場情緒：觀察市場的整體情緒，包括大盤走勢和其他個股的表現。
                    </li>
                    <li>
                      消息面：當日是否有影響市場的重大消息，如公司公告、宏觀經濟數據、國際事件等。
                    </li>
                  </ul>
                </div>
              </td>
            </tr>
            <tr>
              <td>
                <div class="trend-item">
                  <h3>內外盤比例</h3>
                  <p>內外盤比就是在五檔報價上面，一條綠色及紅色的比。</p>
                  <button @click="toggleText($event)">Read more</button>
                  <div class="more-text">
                    <ul>
                      <li>
                        成交在外盤 > 成交在內盤：比較多人用外盤（較貴）的價格成交，代表多數人都搶著買這支股票。
                      </li>
                      <li>
                        成交在內盤 > 成交在外盤：比較多人用內盤（較便宜）的價格成交，代表多數人都搶著賣掉這支股票。
                      </li>
                    </ul>
                  </div>
                </div>
              </td>
              <td>
                <div class="trend-item">
                  <h3>分析K線圖</h3>
                  <p>當日K線的形態可以揭示當日的市場動向。</p>
                  <button @click="toggleText($event)">Read more</button>
                  <div class="more-text">
                    <ul>
                      <li>紅K線（陽線）：表示收盤價高於開盤價，當日價格上漲。</li>
                      <li>綠K線（陰線）：表示收盤價低於開盤價，當日價格下跌。</li>
                      <li>
                        上影線和下影線：影線的長短反映當日價格波動幅度和買賣力量的對比。
                      </li>
                    </ul>
                  </div>
                </div>
              </td>
              <td>
                <div class="trend-item">
                  <h3>成交量</h3>
                  <p>當日成交量相對於前幾日的變化，可以判斷市場參與的積極性。</p>
                  <button @click="toggleText($event)">Read more</button>
                  <div class="more-text">
                    <ul>
                      <li>
                        放量上漲：價格上漲伴隨成交量增加，通常表示市場看好後市。
                      </li>
                      <li>
                        放量下跌：價格下跌伴隨成交量增加，通常表示市場看淡後市。
                      </li>
                    </ul>
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
            <button class="tablinks" @click="openTab($event, 'basic')" id="defaultOpen"><strong>基本術語</strong></button>
            <button class="tablinks" @click="openTab($event, 'transaction')"><strong>交易相關術語</strong></button>
            <button class="tablinks" @click="openTab($event, 'mar')"><strong>市場指標</strong></button>
            <button class="tablinks" @click="openTab($event, 'technical')"><strong>技術分析術語</strong></button>
            <button class="tablinks" @click="openTab($event, 'common')"><strong>其他常見術語</strong></button>
            <button class="tablinks" @click="openTab($event, 'chinese')"><strong>中文特有術語</strong></button>
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
              <!-- 其他術語 -->
            </ul>
          </div>
        </section>
      </main>
    </div>
</template>
  
<script>
  export default {
    name: 'TeachingForm',
    
    mounted() {
      // 添加淡入效果
      this.fadeInTextBlocks();
  
      // 卡片懸停效果
      this.addHoverEffectToCards();
  
      // 初始化標籤頁
      this.initTabs();
  
      // 添加滑入效果
      this.addSlideInEffect();
    },
    methods: {
      fadeInTextBlocks() {
        const textBlocks = document.querySelectorAll('.text-block');
        textBlocks.forEach((el) => {
          el.style.opacity = 0;
          setTimeout(() => {
            el.style.opacity = 1;
          }, 500);
        });
      },
      addHoverEffectToCards() {
        const cards = document.querySelectorAll('.card');
        cards.forEach((el) => {
          el.addEventListener('mouseover', function () {
            this.style.transform = 'scale(1.1)';
          });
          el.addEventListener('mouseout', function () {
            this.style.transform = 'scale(1)';
          });
        });
      },
      toggleText(event) {
        const button = event.currentTarget;
        const moreText = button.nextElementSibling;
        if (moreText.style.display === 'none' || moreText.style.display === '') {
          moreText.style.display = 'block';
          button.textContent = 'Show less';
        } else {
          moreText.style.display = 'none';
          button.textContent = 'Read more';
        }
      },
      initTabs() {
        // 打開默認標籤
        document.getElementById('defaultOpen').click();
      },
      openTab(evt, tabName) {
        let i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName('tabcontent');
        for (i = 0; i < tabcontent.length; i++) {
          tabcontent[i].style.display = 'none';
        }
        tablinks = document.getElementsByClassName('tablinks');
        for (i = 0; i < tablinks.length; i++) {
          tablinks[i].className = tablinks[i].className.replace(' active', '');
        }
        document.getElementById(tabName).style.display = 'block';
        evt.currentTarget.className += ' active';
      },
      addSlideInEffect() {
        const sections = document.querySelectorAll('section');
        const options = {
          threshold: 0.1,
        };
        const observer = new IntersectionObserver((entries, observer) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) {
              return;
            }
            entry.target.classList.add('slide-in');
            observer.unobserve(entry.target);
          });
        }, options);
        sections.forEach((section) => {
          observer.observe(section);
        });
      },
    },
  };
</script>
  
<style scoped>
  header {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-top: 35px;
  }
  
  header img {
    margin-right: 10px;
  }
  
  .header-text {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .separator {
    width: 3px;
    height: 75px;
    background-color: #f8f9fa;
    margin-left: 10px;
    margin-right: 10px;
  }
  
  body {
    font-family: Arial, sans-serif;
    background-color: #f8f9fa;
    color: #333;
    text-align: center;
    margin: 0;
    padding: 0;
    font-weight: bold;
  }
  
  header {
    background-color: #57614e;
    color: #fff;
    padding: 1em 0;
  }
  
  h1 {
    margin: 0;
  }
  
  main {
    padding: 0;
  }
  
  .gray-section {
    background-color: #bdbdbd;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
  }
  
  .beige-section {
    background-color: #e9e9e9;
    padding: 2em;
    margin: 0;
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
    font-size: 50px;
  }
  
  h3 {
    font-size: 32px;
    margin: 1em 0;
    color:#54546c
  }

  h4 {
    font-size: 32px;
    margin: 1em 0;
    color:#f1f1f1
  }
  
  p {
    font-size: 24px;
  }
  
  li {
    font-size: 20px;
  }
  
  .p4 {
    text-align: left;
    font-size: 24px;
  }
  
  .text-block {
    margin: 1em 0;
    padding: 1em;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 200px;
    transition: transform 0.3s, background-color 0.3s;
  }
  
  .card-container {
    display: flex;
    justify-content: space-between;
    margin: 0 auto;
    padding: 0;
    width: 70%;
  }
  
  .card {
    background-color: #fff;
    color: #333;
    padding: 1em;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: transform 0.2s;
    border: 2px solid #333;
    width: 30%;
    margin: 0 0.5em;
  }
  
  .card-content {
    margin-top: 1em;
    text-align: left;
    border-top: 1px solid #333;
    padding-top: 1em;
  }
  
  .text-block1 {
    margin: 1em 0;
    padding: 1em;
    transition: transform 0.3s, background-color 0.3s;
  }
  
  .text-block:hover {
    transform: scale(1.05);
    background-color: #6d6d6a;
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
    background-color: #e9e9e9;
    padding: 1em;
    text-align: left;
  }

  .grid-item.center {
    display: flex;
    flex-direction: column;
    align-items: center; /* 垂直居中 */
    justify-content: center; /* 水平居中 */
    text-align: center; /* 文字水平置中 */
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
  
  /* 自定義按鈕樣式 */
  .trend-item button {
    background-color: #4d4f51; /* 按鈕背景色 */
    color: white; /* 按鈕字體顏色 */
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 5px; /* 圓角 */
    transition: background-color 0.3s ease; /* 添加過渡效果 */
  }

  /* 懸停時的顏色 */
  .trend-item button:hover {
    background-color: #a8aaab; /* 懸停時的背景色 */
  }

  /* 點擊時的顏色 */
  .trend-item button:active {
    background-color: #051a28; /* 點擊時的背景色 */
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
  
  .tab {
    overflow: hidden;
    border-bottom: 1px solid #ccc;
    background-color: #f1f1f1;
    display: flex;
    justify-content: space-between;
    font-size: 24px;
    font-family: Arial, sans-serif;
    margin: 5px 0;
  }

  /* 標籤按鈕的基礎樣式 */
  .tablinks {
    background-color: inherit;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    font-size: 16px;
    color: #34495e; /* 默認字體顏色 */
    transition: color 0.3s ease; /* 變化效果 */
  }

  /* 懸停時的字體顏色 */
  .tablinks:hover {
    color: #3498db; /* 懸停時字體顏色 */
  }

  /* 選中狀態的樣式 */
  .tablinks.active {
    color: #2c3e50; /* 選中時字體顏色 */
    font-weight: bold; /* 讓選中的按鈕字體加粗 */
  }
  
  .tab button {
    background-color: inherit;
    flex: 1;
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
  