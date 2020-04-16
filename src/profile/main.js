import Vue from 'vue'
import ProfilePage from './ProfilePage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(ProfilePage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { ProfilePage }
  }).$mount('#profile-page')
