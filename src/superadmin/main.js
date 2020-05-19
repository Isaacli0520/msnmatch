import Vue from 'vue'
import SuperAdmin from './SuperAdmin.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }
Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
  render: h => h(SuperAdmin),
  vuetify: new Vuetify(vuetifyOptions),
  components: { SuperAdmin }
}).$mount('#superadmin')
