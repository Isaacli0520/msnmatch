import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import MatchPage from './MatchPage.vue'

const vuetifyOptions = { }

Vue.use(Vuetify);


Vue.config.productionTip = false

new Vue({
  render: h => h(MatchPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { MatchPage }
}).$mount('#match')
