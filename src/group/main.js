import Vue from 'vue'
import GroupPage from './GroupPage.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(GroupPage),
  components: { GroupPage }
}).$mount('#group-page')