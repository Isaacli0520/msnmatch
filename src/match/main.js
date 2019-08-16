import Vue from 'vue'
import Match from './Match.vue'
import VueProgressiveImage from 'vue-progressive-image'

Vue.use(VueProgressiveImage, {});


Vue.config.productionTip = false

new Vue({
  render: h => h(Match),
  components: { Match }
}).$mount('#match')