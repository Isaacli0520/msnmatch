import Vue from 'vue'
import MarketMyItemsPage from './MarketMyItemsPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(MarketMyItemsPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { MarketMyItemsPage }
  }).$mount('#market-my-items-page')
