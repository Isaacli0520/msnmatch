import Vue from 'vue'
import ProfileEditPage from './ProfileEditPage.vue'
import Vuetify from 'vuetify/lib'

const vuetifyOptions = { }

Vue.use(Vuetify);

Vue.config.productionTip = false

new Vue({
    render: h => h(ProfileEditPage),
    vuetify: new Vuetify(vuetifyOptions),
    components: { ProfileEditPage }
  }).$mount('#profile-edit-page')
