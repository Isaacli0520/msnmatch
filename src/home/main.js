import Vue from 'vue'
import HomePage from './HomePage.vue'
import {MenuItemGroup, Carousel, CarouselItem,  Menu, Footer, Aside, Submenu, Header, MenuItem, Button , Main, Container,} from 'element-ui';


Vue.use(MenuItemGroup)
Vue.use(Menu)
Vue.use(Carousel)
Vue.use(CarouselItem)
Vue.use(Footer)
Vue.use(Aside)
Vue.use(Header)
Vue.use(MenuItem)
Vue.use(Submenu)
Vue.use(Button)
Vue.use(Main)
Vue.use(Container)

Vue.config.productionTip = false

new Vue({
    render: h => h(HomePage),
    components: { HomePage }
  }).$mount('#home-page')
