import Vue from 'vue'
import ReviewsPage from './ReviewsPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
  render: h => h(ReviewsPage),
  vuetify: vuetify,
  components: { ReviewsPage }
}).$mount('#reviews-page');