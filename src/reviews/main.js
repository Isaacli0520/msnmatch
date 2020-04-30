import Vue from 'vue'
import ReviewsPage from './ReviewsPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = {}

Vue.use(Vuetify);

new Vue({
  render: h => h(ReviewsPage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { ReviewsPage }
}).$mount('#reviews-page');