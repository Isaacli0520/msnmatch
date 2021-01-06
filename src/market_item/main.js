import Vue from 'vue'
import MarketItemPage from './MarketItemPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(MarketItemPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { MarketItemPage }
  }).$mount('#market-item-page')
