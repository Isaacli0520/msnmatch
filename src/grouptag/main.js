import Vue from 'vue'
import GroupTagPage from './GroupTagPage.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(GroupTagPage),
  components: { GroupTagPage }
}).$mount('#group-tag-page')