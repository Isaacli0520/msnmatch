import Vue from 'vue'
import MarketItemPage from './MarketItemPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

Vue.config.productionTip = false

new Vue({
    render: h => h(MarketItemPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { MarketItemPage }
  }).$mount('#market-item-page')
