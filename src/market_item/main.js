import Vue from 'vue'
import MarketItemPage from './MarketItemPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
    render: h => h(MarketItemPage),
    vuetify: vuetify,
    components: { MarketItemPage }
  }).$mount('#market-item-page')
