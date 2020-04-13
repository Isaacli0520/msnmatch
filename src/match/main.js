import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import Match from './Match.vue'
import VueProgressiveImage from 'vue-progressive-image'

const vuetifyOptions = { }

Vue.use(Vuetify);
Vue.use(VueProgressiveImage, {});


Vue.config.productionTip = false

new Vue({
  render: h => h(Match),
  vuetify: new Vuetify(vuetifyOptions),
  components: { Match }
}).$mount('#match')
