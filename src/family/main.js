import Vue from 'vue'
import FamilyPage from './FamilyPage.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(FamilyPage),
  components: { FamilyPage }
}).$mount('#family-page')