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
            <v-spacer v-if="!searchBool"></v-spacer>
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
            color="teal lighten-1"
            :timeout="1800">
            Item Posted
        <v-btn color="cyan accent-1" text @click="success_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red darken-1"
            :timeout="1800">
            Sth is wrong
            <v-btn color="blue" text @click="failure_snack = false"> Close </v-btn>
        </v-snackbar>
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
                            :rules="[v => (v!=undefined && v >= 0) || 'Price is required']"
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
        searchBool:{
            type:Boolean,
            default:false,
        },
        headerUpdate:{
            type:Boolean,
            default:false,
        },
    },
    data: function () {
        return {
            create_item_form_valid:true,
            createItemBtnLoading:false,
            createItemDialog:false,
            query:"",
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
                    'value':'rentals',
                    'text':'Rentals'
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
                { title:"Edit Profile", icon:"fas fa-biohazard" },
                { title:"Log Out", icon:"fas fa-angry"},
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
                    "title":"Rentals",
                    "icon":"fas fa-house-user",
                    "href":"/market/?c=rentals",
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
        createItem(item){
            this.$refs.create_form.validate();
            if(!this.create_item_form_valid)
                return;
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
                if(response.data.success){
                    // this.$message({
                    //     message: 'Item Posted',
                    //     type: 'success'
                    // });
                    this.success_snack = true;
                    this.createItemBtnLoading = false;
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
                    // this.$message({
                    //     message: 'Sth is wrong',
                    //     type: 'error'
                    // });
                }
            });
        },
        searchItem(query){
            let tmp_url = window.location.pathname.substr(0,window.location.pathname.lastIndexOf('/'));
            if(tmp_url == "/market/items")
                this.goToHref('/market/' + '?q=' + query);
            else{
                let url = new URL(window.location.href);
                url.searchParams.set('q', query);
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