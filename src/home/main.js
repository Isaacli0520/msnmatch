import Vue from 'vue'
// import '../plugins/vuetify'
import HomePage from './HomePage.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(HomePage),
  components: { HomePage }
}).$mount('#home-page')