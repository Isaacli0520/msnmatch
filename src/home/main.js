import Vue from 'vue'
import HomePage from './HomePage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

Vue.config.productionTip = false

new Vue({
    render: h => h(HomePage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { HomePage }
  }).$mount('#home-page')
