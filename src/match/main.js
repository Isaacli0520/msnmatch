import Vue from 'vue'
import Match from './Match.vue'


Vue.config.productionTip = false

new Vue({
  render: h => h(Match),
  components: { Match }
}).$mount('#match')