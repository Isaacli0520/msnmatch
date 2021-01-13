import Vue from 'vue'
import CommentFilterPage from './CommentFilterPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(CommentFilterPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CommentFilterPage }
}).$mount('#comment-filter-page');