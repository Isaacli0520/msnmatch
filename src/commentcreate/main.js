import Vue from 'vue'
import CommentCreatePage from './CommentCreatePage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(CommentCreatePage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CommentCreatePage }
}).$mount('#comment-create-page');