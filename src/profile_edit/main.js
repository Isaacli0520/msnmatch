import Vue from 'vue'
import ProfileEditPage from './ProfileEditPage.vue'
import vuetify from '../plugins/vuetify'

new Vue({
    render: h => h(ProfileEditPage),
    vuetify: vuetify,
    components: { ProfileEditPage }
  }).$mount('#profile-edit-page')
