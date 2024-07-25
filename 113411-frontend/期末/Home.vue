<template>
  <div class="dashboard">
    <div class="content-left">
      <h1>台股指數</h1>
      <iframe src="https://s.yimg.com/nb/tw_stock_frontend/scripts/TseChart/TseChart.eb1b267900.html" width="80%" height="500px" frameborder="0"></iframe>
      <div class="description">
                <button class="accordion">台股大盤是什麼？</button>
                <div class="panel">
                      <p>台灣股市的整體表現，也就是我們常聽到的「大盤」，也叫做「加權指數」。<br>如果今天大盤是往上漲的，代表今天大部分的股票是上漲的（但還是會有下跌的個股）；反之如果大盤下跌，我們就可以預想到，今天個股整體表現來說是差的，所以我們看大盤就可以大概知道今天股市的表現！<br><br>那麼為什麼又叫做「加權指數」呢？<br>加權指數指的是「指數」透過「加權」的方式計算出一個值，用來觀察股市的整體情況，而台灣的加權股價指數是用「市值」來加權，也就是說股票市值越高，對指數的影響就越大。</p>
                </div>
                <button class="accordion">大盤與個股的關係</button>
                <div class="panel">
                      <p>對於投資者來說，大盤指數更像是展現股市氛圍的一種指標，比如說大盤向上漲，投資者對於市場上的股票就會比較看好，在這樣的環境下，很容易帶起一種樂觀的上漲氣氛，比如往往會發現平時一些沒怎麼在漲的股票也悄悄漲了起來，或是有些小漲的股票居然多漲了一些。反過來說當大盤下跌的時候，因投資者們憂心整體股市表現不佳，就會更容易傾向於賣出手上的股票，在跌的股票可能會賣的更兇。<br><br>這種就會形成大盤強就容易帶著個股上漲，大盤弱就容易帶著個股下跌的情況非常常見，因此在交易的時候，一定要觀察大盤指數，了解整體股市的表現，對於交易決策者來說，有可能起到至關重要的一環。<br><br>但一定要記得，大盤只是一個總體氣氛的指標，如果股票表現不好或最近有出現利空消息，仍然可能與大盤的方向背道而馳，並不是大盤上漲就一定可以扭轉個股的走勢，大盤跟個股兩者之間，比較容易呈現一種錦上添花疊加的作用。</p>
                </div>
                <button class="accordion">台灣指數成分股有哪些？</button>
                <div class="panel">
                      <p>台股大盤指數涵蓋了上市於台灣證券交易所的所有企業，包括源自於各行各業的公司，它的成分股構成會根據統計方式進行定期調整，例如只有上市超過一個月的企業才會被納入統計。<br><br>目前上市於台灣證券交易所的企業有900多家，其中前二十大企業股價佔據了超過50% 的權重量。以下是截止於2024年5月的台灣加權指數十大成分股和其權重：</p>
                      <table>
          <thead>
            <tr>
              <th>排行</th>
              <th>證券名稱</th>
              <th>市值佔 大盤比重</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>2330	台積電</td>
              <td>31.7964%	</td>
            </tr>
            <tr>
              <td>2</td>
              <td>2317	鴻海</td>
              <td>3.5607%		</td>
            </tr>
            <tr>
              <td>3</td>
              <td>2454	聯發科</td>
              <td>2.9501%	</td>
            </tr>
            <tr>
              <td>4</td>
              <td>2382	廣達</td>
              <td>1.5805%		</td>
            </tr>
            <tr>
              <td>5</td>
              <td>2412	中華電</td>
              <td>1.4828%		</td>
            </tr>
            <tr>
              <td>6</td>
              <td>2881	富邦金</td>
              <td>1.4266%	</td>
            </tr>
            <tr>
              <td>7</td>
              <td>2308	台達電</td>
              <td>1.2606%	</td>
            </tr>
            <tr>
              <td>8</td>
              <td>2882	國泰金</td>
              <td>1.2311%		</td>
            </tr>
            <tr>
              <td>9</td>
              <td>2891	中信金</td>
              <td>1.0373%	</td>
            </tr>
            <tr>
              <td>10</td>
              <td>3711	日月光投控	</td>
              <td>1.0298	</td>
            </tr>
            
          </tbody>
        </table>
                
                    </div>
      </div>
    </div>
    <div class="content-right">
      <h2>AI 推薦股票</h2>
      <p></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  components: {},
  data() {
    return {
      chartData: null
    };
  },
  mounted() {
    var acc = document.getElementsByClassName("accordion");
    var i;

    for (i = 0; i < acc.length; i++) {
      acc[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
          panel.style.display = "none";
        } else {
          panel.style.display = "block";
        }
      });
    }
  }
}
</script>

<style scoped>
h1,
h2 {
  text-align: center;
}

.dashboard {
  margin-top: 30px;
  display: flex;
  padding: 20px;
  margin-bottom: 20px; 
}

.content-left {
  flex: 6;
  padding-right: 10px;
  justify-content: center;
}

.description {
  margin-top: 10px; /* 確保文字說明與iframe之間有適當的間距 */
}

.content-right {
  flex: 4;
}

.footer {
  display: flex;
  justify-content: center;
  padding: 10px 0;
  background-color: #f4f4f4;
  margin-top: 20px;
}

.footer-link {
  margin: 0 10px;
  text-decoration: none;
  color: #007bff;
}

.footer-link:hover {
  text-decoration: underline;
}

p {
  font-size: 18px;
  text-align: left;
}
button.accordion{
  font-size: 20px;
  color: #0c0c0c;
  background-color: rgb(241, 241, 241);
}
.accordion {
    background-color: #eee;
    color: #444;
    cursor: pointer;
    padding: 10px;
    width: 100%;
    text-align: left;
    border: none;
    outline: none;
    transition: 0.4s;
    margin: 5px 0;
}
tr, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
  word-wrap: break-word;
}
</style>
