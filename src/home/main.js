import Vue from 'vue'
import HomePage from './HomePage.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

Vue.use(Vuetify);
Vue.prototype.$message = Message;

const vuetifyOptions = { 
  
}

Vue.config.productionTip = false

new Vue({
    render: h => h(HomePage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { HomePage }
  }).$mount('#home-page')
