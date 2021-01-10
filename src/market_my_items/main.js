import Vue from 'vue'
import MarketMyItemsPage from './MarketMyItemsPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
    render: h => h(MarketMyItemsPage),
    vuetify: vuetify,
    components: { MarketMyItemsPage }
  }).$mount('#market-my-items-page')
