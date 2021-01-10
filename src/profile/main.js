import Vue from 'vue'
import ProfilePage from './ProfilePage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
    render: h => h(ProfilePage),
    vuetify: vuetify,
    components: { ProfilePage }
  }).$mount('#profile-page')
