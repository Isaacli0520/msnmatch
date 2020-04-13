import Vue from 'vue'
import MarketCategoryPage from './MarketCategoryPage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

Vue.config.productionTip = false

new Vue({
    render: h => h(MarketCategoryPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { MarketCategoryPage }
  }).$mount('#market-category-page')
