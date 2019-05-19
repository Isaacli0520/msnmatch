import Vue from 'vue'
// import '../plugins/vuetify'
import TagPage from './TagPage.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(TagPage),
  components: { TagPage }
}).$mount('#tag-page')