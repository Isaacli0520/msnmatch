import Vue from 'vue'
import MarketPage from './MarketPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

Vue.config.productionTip = false

new Vue({
    render: h => h(MarketPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { MarketPage }
  }).$mount('#market-page')
