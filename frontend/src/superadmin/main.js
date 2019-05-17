import Vue from 'vue'
// import '../plugins/vuetify'
import SuperAdmin from './SuperAdmin.vue'


Vue.config.productionTip = false

new Vue({
  render: h => h(SuperAdmin),
  components: { SuperAdmin }
}).$mount('#superadmin')
