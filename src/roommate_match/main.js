import Vue from 'vue'
import RoommateMatchPage from './RoommateMatchPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(RoommateMatchPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { RoommateMatchPage }
  }).$mount('#roommate-match-page')
