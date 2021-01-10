import Vue from 'vue'
import MarketPage from './MarketPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
    render: h => h(MarketPage),
    vuetify: vuetify,
    components: { MarketPage }
  }).$mount('#market-page')
