import Vue from 'vue'
import '../plugins/vuetify'
import HomePage from './HomePage.vue'

Vue.config.productionTip = false

new Vue({
  el: '#home-page',
  render: h => h(HomePage),
  components: { HomePage }
})