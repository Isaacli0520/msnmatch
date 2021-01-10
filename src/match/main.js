import Vue from 'vue'
import vuetify from '../plugins/vuetify'
import MatchPage from './MatchPage.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(MatchPage),
  vuetify: vuetify,
  components: { MatchPage }
}).$mount('#match')
