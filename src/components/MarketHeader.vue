<template>
    <div>
        <v-navigation-drawer
            light
            color="white"
            app
            v-model="drawer"
            :clipped="$vuetify.breakpoint.mdAndUp"
            >
            <v-list dense>
                <v-list-item
                    :key="index_item + '-trash' " 
                    v-for="(item, index_item) in main_items"
                    :href="item.href"
                    :target="item.target">
                    <v-list-item-avatar
                        v-if="item.icon">
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content>
                        <v-list-item-title class="font-weight-bold">{{ item.title }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item @click="createItemDialog=true;">
                    <v-list-item-avatar>
                        <v-icon>fas fa-dollar-sign</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content>
                        <v-list-item-title class="font-weight-bold">Sell an Item</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-list dense>
                <v-list-item
                    :key="index_item + '-trash' " 
                    v-for="(item, index_item) in category_items"
                    :href="item.href"
                    :target="item.target">
                    <v-list-item-avatar
                        v-if="item.icon">
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content>
                        <v-list-item-title class="font-weight-bold">{{ item.title }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
        <v-app-bar
            :clipped-left="$vuetify.breakpoint.mdAndUp"
            app
            light
            height="62"
            
            elevation="1"
            >
            <v-app-bar-nav-icon  @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-img max-height="46" max-width="46" :src="urls.brand_pic" alt=""></v-img>
            <v-toolbar-items v-if="$vuetify.breakpoint.mdAndUp">
                <v-btn 
                    :href="urls.market_url"
                    text>Market</v-btn>
                <!-- <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="urls.market_url"
                    text>Sell</v-btn> -->
            </v-toolbar-items>
            <v-text-field
                label="Search Item"
                v-model="query"
                v-on:keyup.enter="searchItem(query)"
                color="grey lighten-5"
                background-color="blue-grey lighten-5"
                clearable
                light
                solo-inverted
                no-filter
                flat
                hide-no-data
                hide-selected
                hide-details
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-menu offset-y
                class="mx-auto"
                min-width="170">
                <template v-slot:activator="{ on }">
                    <v-btn
                        icon
                        v-on="on">
                        <v-icon>mdi-apps</v-icon>
                    </v-btn>
                </template>
                <v-list dense rounded>
                    <v-list-item
                        v-for="(item, index) in app_items"
                        :key="index + '-app'"
                        @click="navMethod(item)">
                        <v-list-item-icon>
                            <v-icon dense v-text="item.icon"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-menu>
            <v-menu offset-y
                class="mx-auto"
                min-width="170">
                <template v-slot:activator="{ on }">
                    <v-btn
                        icon
                        v-on="on">
                        <v-icon>fas fa-user-circle</v-icon>
                    </v-btn>
                </template>
                <v-list dense rounded>
                    <v-list-item
                        v-for="(item, index) in user_items"
                        :key="index"
                        @click="navMethod(item)">
                        <v-list-item-icon>
                            <v-icon dense v-text="item.icon"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-app-bar>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="2700">
            Item Posted
        <v-btn color="cyan accent-1" text @click="success_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="form_failure_snack"
            color="red lighten-1"
            :timeout="2700">
            Invalid Form
            <v-btn color="white" text @click="form_failure_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red lighten-1"
            :timeout="2700">
            Sth is wrong
            <v-btn color="white" text @click="failure_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-dialog v-model="disclaimerDialog" persistent scrollable min-width="150px" max-width="450px">
            <v-card>
                <v-card-title>Disclaimer</v-card-title>
                <v-divider></v-divider>
                <v-card-text style="margin-top:10px;white-space:pre-wrap;">
                    {{disclaimerText}}
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" text @click="goToHref('/')">Disagree</v-btn>
          <v-btn color="green darken-1" text @click="agreeDisclaimer">Agree</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="createItemDialog" scrollable min-width="350px" max-width="600px">
            <v-card>
                <v-card-title>Sell an Item</v-card-title>
                <v-divider></v-divider>
                <v-card-text style="height: 600px;">
                    <v-form
                        ref="create_form"
                        v-model="create_item_form_valid">
                        <v-text-field
                        v-model="item.name"
                        :counter="25"
                        :rules="nameRules"
                        label="Name"
                        required
                        ></v-text-field>

                        <v-text-field
                            v-model="item.price"
                            label="Price (Dollars)"
                            :rules="priceRules"
                            required
                            type="number"
                        />

                        <v-select
                        v-model="item.condition"
                        :items="conditions"
                        :rules="[v => !!v || 'Condition is required']"
                        label="Condition"
                        required
                        ></v-select>

                        <v-select
                        v-model="item.category"
                        :items="categories"
                        :rules="[v => !!v || 'Category is required']"
                        label="Category"
                        required
                        ></v-select>

                        <v-file-input 
                        v-model="item.image"
                        accept="image/*"
                        label="Image"></v-file-input>

                        <v-checkbox
                        v-model="item.pickup"
                        label="Pickup"
                        ></v-checkbox>

                        <v-checkbox
                        v-model="item.delivery"
                        label="Delivery"
                        ></v-checkbox>

                        <v-textarea
                            v-model="item.description"
                            label="Description"
                            outlined
                            :rules="descriptionRules"
                            required
                            rows="3"
                            row-height="20"
                        ></v-textarea>
                    </v-form>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" :loading="createItemBtnLoading" outlined @click.prevent="createItem(item)">Create</v-btn>   
                    <v-btn color="blue darken-1" outlined @click="createItemDialog = false">Close</v-btn> 
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import axios from 'axios'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default{
    props: {
    },
    data: function () {
        return {
            disclaimerDialog:false,
            disclaimerVersion:0.1,
            disclaimerText:
            `1. MSN Market提供二手物品信息发布平台，我们会尽量排除不良卖家，但无法对信息的真实性逐一验证，购买二手物品请仔细辨别。
2. 交易双方自行承担交易风险和因此产生的经济损失，MSN不为交易产品信息的可靠性、准确性和产品质量承担任何责任。
3. 疫情期间，建议尽量减少接触。

发帖须知
1. 请在售卖物品时填写对应的类别，新旧程度，物品详细描述，实物照片，价格，卖家联系方式
2. 标题规则：需注明 物品+数量，例：玻璃花瓶2个
3. 物品售出后，请将物品状态设置为Sold

严禁以下行为（违规将被删除及警告）
1. 禁止出售违禁品
2. 禁止出售高于原价的产品
3. 禁止非交易类帖子
4. 禁止多次重复发布内容相同的帖子
5. 禁止出售假货`,
            create_item_form_valid:true,
            createItemBtnLoading:false,
            createItemDialog:false,
            query:"",
            form_failure_snack:false,
            success_snack:false,
            failure_snack:false,
            navDrawer:false,
            drawer: null,
            item:{
                name:"",
                price:0,
                condition:'new',
                category:'miscellaneous',
                pickup:false,
                delivery:false,
                description:"",
                image:null,
            },
            priceRules:[
                v => (v != undefined && v!="" && (v || v == 0) && v >= 0) || 'Price is required',
                v => (this.countDecimals(v) <= 2) || 'Should be <= 2 decimal places',
                v => (v <= 500000) || 'Are you serious?',
            ],
            nameRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 25) || 'Name must be less than 25 characters',
            ],
            descriptionRules: [
                v => !!v || 'Desctiption is required',
                v => (v && v.length <= 350) || 'Desctiption must be less than 350 characters',
            ],
            conditions:[
                {   
                    'value':'new',
                    'text':'New'
                },
                {   
                    'value':'slightlyused',
                    'text':'Slightly Used'
                },
                {   
                    'value':'used',
                    'text':'Used'
                },
                {   
                    'value':'dysfunctional',
                    'text':'Dysfunctional'
                },
            ],
            categories:[
                {   
                    'value':'electronics',
                    'text':'Electronics'
                },
                {   
                    'value':'textbooks',
                    'text':'Textbooks'
                },
                {   
                    'value':'furniture',
                    'text':'Furniture'
                },
                {   
                    'value':'schoolsupplies',
                    'text':'School supplies'
                },
                {   
                    'value':'clothing',
                    'text':'Clothing'
                },
                {   
                    'value':'housing',
                    'text':'Housing'
                },
                {   
                    'value':'pets',
                    'text':'Pet Supplies'
                },
                {   
                    'value':'miscellaneous',
                    'text':'Miscellaneous'
                },
            ],
            navBarItems:[
                {
                    text:"HoosMyProfessor",
                    href:"",
                    diabled:true,
                },
                {
                    text:"Match",
                    href:"",
                    diabled:true,
                },
            ],
            user_items:[
                { title:"Profile", icon:"fas fa-user" },
                { title:"Edit Profile", icon:"fas fa-user-edit" },
                { title:"Log Out", icon:"fas fa-sign-out-alt"},
            ],
            app_items:[
                { title:"Match", icon:"fas fa-user-friends" },
                { title:"HoosMyProfessor", icon:"fas fa-graduation-cap" },
                { title:"Live Comments", icon:"fas fa-comment" },
            ],
            urls:{
                home_url:"",
                brand_pic:"",
                profile:"",
                update_profile:"",
                logout:"",
                my_courses:"",
                market_url:"",
                courses_url:"",
                match_url:"",
                comment_url:"",
            },
            main_items:[
                {
                    "title":"Home",
                    "icon":"fas fa-home",
                    "href":"/market/",
                    "target":"",
                },
                {
                    "title":"My Items",
                    "icon":"fas fa-list-ul",
                    "href":"/market/items/",
                    "target":"",
                }],
            category_items:[
                {
                    "title":"Electronics",
                    "icon":"fas fa-bolt",
                    "href":"/market/?c=electronics",
                    "target":"",
                },
                {
                    "title":"Textbooks",
                    "icon":"fas fa-book",
                    "href":"/market/?c=textbooks",
                    "target":"",
                },
                {
                    "title":"Furniture",
                    "icon":"fas fa-house-user",
                    "href":"/market/?c=furniture",
                    "target":"",
                },
                {
                    "title":"School Supplies",
                    "icon":"fas fa-school",
                    "href":"/market/?c=schoolsupplies",
                    "target":"",
                },
                {
                    "title":"Pet Supplies",
                    "icon":"fas fa-cat",
                    "href":"/market/?c=pets",
                    "target":"",
                },
                {
                    "title":"Clothing",
                    "icon":"fas fa-tshirt",
                    "href":"/market/?c=clothing",
                    "target":"",
                },
                {
                    "title":"Housing",
                    "icon":"fas fa-bed",
                    "href":"/market/?c=housing",
                    "target":"",
                },
                {
                    "title":"Miscellaneous",
                    "icon":"fas fa-question",
                    "href":"/market/?c=miscellaneous",
                    "target":"",
                },
            ],
            old_items: [
                { icon: 'fas fa-book', text: 'HoosMyProfessor' },
                { icon: 'fas fa-user', text: 'Match' },
                ],
        }
    },
    components:{
    },
    watch:{
    },
    computed:{
    },
    methods:{
        countDecimals(value) { 
            if ((value % 1) != 0 || value.toString().indexOf(".") != -1) 
                return value.toString().split(".")[1].length;  
            return 0;
        },
        setCookie(name,value,days) {
            var expires = "";
            if (days) {
                var date = new Date();
                date.setTime(date.getTime() + (days*24*60*60*1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "")  + expires + "; path=/";
        },
        getCookie(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
            return null;
        },
        eraseCookie(name) {   
            document.cookie = name+'=; Max-Age=-99999999;';  
        },
        agreeDisclaimer(){
            this.eraseCookie('msn-market-disclaimer');
            this.setCookie('msn-market-disclaimer', this.disclaimerVersion, 365);
            this.disclaimerDialog = false;
            this.$emit("accept-disclaimer");
        },
        createItem(item){
            this.$refs.create_form.validate();
            if(!this.create_item_form_valid){
                this.form_failure_snack = true;
                return;
            }
            this.createItemBtnLoading = true;
            let formData = new FormData();
            formData.append('image',item.image);
            for(var key in item){
                if(key != "image"){
                    formData.append(key, item[key]);
                }
            }
            axios.post('/market/api/create_item/',formData,
            {
                headers:{
                    'Content-Type': 'multipart/form-data',
                }
            }).then(response => {
                this.createItemBtnLoading = false;
                if(response.data.success){
                    this.success_snack = true;
                    this.$emit('update-items');
                    this.createItemDialog = false;
                    this.item = {
                        name:"",
                        price:0,
                        condition:'new',
                        category:'miscellaneous',
                        pickup:false,
                        delivery:false,
                        description:"",
                        image:null,
                    };
                    this.$refs.create_form.resetValidation();
                }else{
                    this.failure_snack=true;
                }
            });
        },
        escapeString(unsafe) {
            return unsafe
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        },
        searchItem(query){
            // let tmp_url = window.location.pathname.substr(0,window.location.pathname.lastIndexOf('/'));
            if(window.location.pathname.startsWith("/market/item"))
                this.goToHref('/market/' + '?q=' + this.escapeString(query));
            else{
                let url = new URL(window.location.href);
                url.searchParams.set('q', this.escapeString(query));
                this.goToHref(url);
            }
        },
        navAsideMethod(item){
            if(item.text == "HoosMyProfessor"){
                this.goToHref(this.urls.courses_url);
            }
            else if(item.text == "Match"){
                this.goToHref(this.urls.match_url);
            }
        },
        navMethod(item){
            if(item.title=="Profile"){
                this.goToHref(this.urls.profile)
            }
            else if(item.title=="Edit Profile"){
                this.goToHref(this.urls.update_profile)
            }
            else if(item.title=="Log Out"){
                this.goToHref(this.urls.logout)
            }
            else if(item.title=="Match"){
                this.goToHref(this.urls.match_url)
            }
            else if(item.title=="Live Comments"){
                this.goToHref(this.urls.comment_url)
            }
            else if(item.title == "HoosMyProfessor"){
                this.goToHref(this.urls.courses_url);
            }
        },
        get_basic_info(){
            axios.get('/courses/ajax/get_basic_info/',{params: {}}).then(response => {
                this.urls = response.data.all_info;
                this.navBarItems[0] = {
                    text:"HoosMyProfessor",
                    href:this.urls.courses_url,
                    diabled:false,
                };
                this.navBarItems[1] = {
                    text:"Match",
                    href:this.urls.match_url,
                    diabled:false,
                };
            });
        },
        goToHref(text){
            window.location.href = text;
        },
    },
    mounted(){
        this.get_basic_info();
        let tmp_cookie = this.getCookie('msn-market-disclaimer');
        // console.log("Cookie", tmp_cookie);
        if(!tmp_cookie || tmp_cookie != this.disclaimerVersion){
            this.disclaimerDialog = true;
        }else{
            this.$emit("accept-disclaimer");
        }

    },
}
</script>


<style lang="css">
    .theme--light.v-app-bar.v-toolbar.v-sheet{
        background-color: white !important;
    }
    .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot .v-label, .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot input {
        color: #000000 !important;
    }

</style>