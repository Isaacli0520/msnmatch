import Vue from 'vue'
import MarketPage from './MarketPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(MarketPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { MarketPage }
  }).$mount('#market-page')
