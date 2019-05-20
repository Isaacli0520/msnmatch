import Vue from 'vue'
// import '../plugins/vuetify'
import TagsPage from './TagsPage.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(TagsPage),
  components: { TagsPage }
}).$mount('#tags-page')