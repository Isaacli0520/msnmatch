import Vue from 'vue'
import GroupsManagePage from './GroupsManagePage.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(GroupsManagePage),
  components: { GroupsManagePage }
}).$mount('#groups-manage-page')