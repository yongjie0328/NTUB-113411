<template>
  <div class="content">
    <h2>投資評估</h2>

    <div v-for="(question, index) in questions" :key="index">
      <p class="question">{{ question.text }}</p>
      <div v-for="(option, optionIndex) in question.options" :key="optionIndex" style="text-align: left;">
        <input type="radio" :id="'option'+optionIndex" :value="optionIndex" v-model="selectedOptions[index]">
        <label :for="'option'+optionIndex">{{ option }}</label>
      </div>
      <hr>
    </div>

    <button @click="submit" class="submit-button">提交</button>
  </div>
</template>

<script>
export default {
  name: 'TeachingAssessment',
  data() {
    return {
      questions: [
        {
          text: "1.你的投資目標是什麼？是增長資本、收穫收益還是分散風險？",
          options: ["增長資本", "收穫收益", "分散風險"],
          selectedOption: null
        },
        {
          text: "2.你的投資時間框架是多長？你打算在多久的時間內實現你的投資目標？",
          options: ["短期（1年內）", "中期（1-5年）", "長期（5年以上）"],
          selectedOption: null
        },
        {
          text: "3.你的風險承受能力如何？你願意承受多大程度的波動和潛在虧損？",
          options: ["低風險", "中風險", "高風險"],
          selectedOption: null
        },
        {
          text: "4.你對不同類型的投資（股票、債券、基金、房地產等）有多少了解？你對這些投資的風險和潛在回報有什麼看法？",
          options: ["股票", "債券", "基金", " 房地產"],
          selectedOption: null
        },
        {
          text: "5.你對目前的市場環境有什麼看法？你認為哪些行業或資產類別有潛在增長機會？",
          options: ["技術", "醫療保健", "能源", "金融","消費品"],
          selectedOption: null
        },
        {
          text: "6.你是否有一個明確的退出策略？在何種情況下你會考慮賣出你的投資？",
          options: ["達到預期收益率", " 遇到特定的停損點", "出現不利的基本面情況"],
          selectedOption: null
        },
        {
          text: "7.你對公司的基本面有多少了解？你會查看哪些指標和資訊來評估一家公司的價值？",
          options: ["企業盈利", " 負債水平", "行業地位","競爭優勢"],
          selectedOption: null
        },
        {
          text: "8.你是否有一個明確的退出策略？在何種情況下你會考慮賣出你的投資？",
          options: ["達到預期收益率", "遇到特定的停損點", "出現不利的基本面情況"],
          selectedOption: null
        },
        
      ],
      selectedOptions: [] // Store selected options
    };
  },
  methods: {
    submit() {
      // Handle submission, you can access selectedOptions array here
      console.log("Selected options:", this.selectedOptions);
      // You can perform further actions here, such as sending data to server or processing it
    }
  }
};
</script>

<style scoped>
.content {
width: 100%;
max-height: 85vh; /* Limiting the height */
overflow-y: auto; /* Adding vertical scrollbar if needed */
margin: 0 auto; /* Center the content horizontally */
}

.question {
  text-align: left;
}

.submit-button {
  padding: 10px 15px; /* Adjust padding to increase button size */
  font-size: 16px; /* Adjust font size */
}
</style>
