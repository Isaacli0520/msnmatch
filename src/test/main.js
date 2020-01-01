import Vue from 'vue'
import Test from './Test.vue'
import Vuetify from 'vuetify/lib'
import {Message} from 'element-ui'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.prototype.$message = Message;

new Vue({
  render: h => h(Test),
  vuetify: new Vuetify(vuetifyOptions),
  components: { Test }
}).$mount('#test-page');