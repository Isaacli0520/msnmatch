import Vue from 'vue'
import CommentsPage from './CommentsPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

new Vue({
  render: h => h(CommentsPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CommentsPage }
}).$mount('#comments-page');