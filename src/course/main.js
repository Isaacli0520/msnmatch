import Vue from 'vue'
import CoursePage from './CoursePage.vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify);
// import {MenuItemGroup, Carousel, CarouselItem,  Menu, Footer, Aside, Submenu, Header, MenuItem, Button , Main, Container,} from 'element-ui';


// Vue.use(MenuItemGroup)
// Vue.use(Menu)
// Vue.use(Carousel)
// Vue.use(CarouselItem)
// Vue.use(Footer)
// Vue.use(Aside)
// Vue.use(Header)
// Vue.use(MenuItem)
// Vue.use(Submenu)
// Vue.use(Button)
// Vue.use(Main)
// Vue.use(Container)

const vuetifyOptions = { 
  
}

new Vue({
  render: h => h(CoursePage),
  vuetify: new Vuetify(vuetifyOptions),
  components: { CoursePage }
}).$mount('#course-page');