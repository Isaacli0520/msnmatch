<template>
    <v-app>
        <match-header
            :headerUpdate="headerUpdate"></match-header>
        <v-main class="content-div">
            <v-container 
                class="fill-height"
                v-if="!loaded">
                <v-row justify="center" align="center">
                    <div>
                        <v-progress-circular
                        :size="60"
                        :width="6"
                        indeterminate
                        color="teal lighten-1">
                        </v-progress-circular>
                    </div>
                </v-row>
            </v-container>
            <v-container v-if="loaded">
                <div class="top-part-wrapper">
                    <v-row justify="center">
                        <div style="text-align: center;">
                            <!-- <h1 class="title-text">MSN Mentor-Mentee Match</h1> -->
                            <h1 class="title-text">Roommate Match</h1>
                            <!-- <h4 class="subtitle-text">Search for existing tags or add your own tags</h4> -->
                        </div>
                    </v-row>
                    <v-row>
                        <div class="search-tags mb-3">
                            <span :key="index" v-for="(tag,index) in tags"
                                class="search-tag">
                                <span>{{tag}}</span>
                                <span class="search-tag-remove"><i v-on:click="del_tag(tag)" class="fas fa-times"></i></span>
                            </span>
                        </div>
                    </v-row>
                    <v-row justify="center">
                        <div class="search-form mt-1">
                            
                            <input 
                                @keydown="onKeydown" 
                                v-model="query" 
                                autocomplete="off" 
                                id="myInput" 
                                type="text" 
                                name="class" 
                                placeholder=" &quot;Marvel&quot;, &quot;major:Math&quot;, &quot;loc:Beijing&quot; " 
                                class=" search-input" 
                                aria-label="Search">
                        </div>
                    </v-row>
                    <v-row justify="center" v-if="!request_user.rm">
                        <div style="text-align:center; margin-top:18px;">
                            <v-btn outlined color="teal lighten-1" @click="openRoleDialog(true)">Find Roommates</v-btn>
                        </div>
                    </v-row>
                    <v-row justify="center" v-if="request_user.rm">
                        <div style="text-align:center; margin-top:18px;">
                            <v-btn outlined color="teal lighten-1" @click="openRoleDialog(false)">Roommates Found</v-btn>
                        </div>
                    </v-row>
                    <v-row justify="center">
                        <div v-if="!request_user.rm " style="text-align:center;">
                            <small class="muted-text">*Note that you have to click the above button to appear in the user list and perform any actions</small>
                        </div>
                    </v-row>
                </div>
                <v-row>
                    <v-col
                        v-for="(user, i) in users"
                        :key="i"
                        cols="12"
                        sm="6"
                        md="4"
                        lg="4"
                        xl="3">
                        <user-card
                            class="fill-height"
                            :display_role="false"
                            :user_index="i"
                            :user="user" @open-user-dialog="openUserDialog"></user-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
        <user-dialog
            v-if="d_user"
            :edit="request_user.username == d_user.username"
            :rm="true"
            :user="d_user"
            v-model="userDialog"></user-dialog>
        <v-dialog v-model="roleDialog" scrollable min-width="200px" max-width="600px">
            <v-card>
                <v-card-title>{{request_user && request_user.rm ? "Roommates Found" : "Find Roommates"}}</v-card-title>
                <v-divider></v-divider>
                <v-card-text v-if="request_user && !request_user.rm"  style="color:black;margin-top:21px; font-size:16px;font-weight:500;">
                    <p>本页面旨在帮助大家寻找合适的室友，如果想找室友的话可以点击下方的Yes即可出现在下面的List中</p>
                    <p>我们在Profile中提供了<strong>Roommate Bio和作息时间</strong>来帮助大家更好的找到适合自己的室友</p>
                    <p>希望想找室友的同学可以去Edit Profile认真填写这两项</p>
                    <p><strong>Do you really want to find roommates</strong>?</p>
                </v-card-text>
                <v-card-text v-if="request_user && request_user.rm" style="color:black;margin-top:21px; font-size:16px;font-weight:500;">
                    <p>如果你已经找到室友了，那么点击Yes后你就不会出现在下面的List中啦！</p>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" :loading="roleBtnLoading" outlined @click="setRoommateRole(dialogRole)">Yes</v-btn>
                    <v-btn color="red lighten-1" outlined @click="roleDialog = false">No</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="1800">
            {{success_text}}
        <v-btn color="cyan accent-1" text @click="success_snack = false"> Close </v-btn></v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red lighten-1"
            :timeout="2700">
            {{failure_text}}
        <v-btn color="white" text @click="failure_snack = false"> Close </v-btn></v-snackbar>
    </v-app>
</template>

<script>
import Vue from "vue";
import axios from 'axios'
import { MatchHeader, UserCard, UserDialog } from '../components'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
	data() {
        return {
            loaded:false,
            // Header
            headerUpdate: false,
            // Search Bar
            query:"",
            tags:[],
            // Users
            request_user:null,
            users:[],
            backup_all_users: [],
            // Dialog
            dialogRole:"Mentor",
            roleBtnLoading:false,
            userDialog:false,
            roleDialog:false,
            dialog_user_index:-1,
            // Fuzz Search
            fuzz: null,
            options:null,
            // Snacks
            failure_text:"",
            success_text:"",
            failure_snack:false,
            success_snack:false,
        }
	},
	components:{
        MatchHeader,
        UserCard,
        UserDialog,
	},
	watch: {
        tags(val){
            this.user_list_filter(val);
        }
	},
	computed:{
        d_user(){
            if(this.dialog_user_index < 0)
                return null;
            else
                return this.users[this.dialog_user_index];
        },
	},
	methods: {
        setRoommateRole(rm){
            this.roleBtnLoading = true;
            axios.post('/skills/api/choose_roommate_role/',{"rm":rm}).then(response => {
                this.roleDialog = false;
                this.roleBtnLoading = false;
                if(response.data.success){
                    this.success_text = "Success";
                    this.success_snack = true;
                    this.getAllUsers();
                }
                else{
                    this.failure_text = "Sth is wrong. 你似乎发现了神奇的bug";
                    this.failure_snack = true;
                }
            });
            
        },
        openRoleDialog(role){
            this.dialogRole = role;
            this.roleDialog = true;
        },
        add_tag(tag){
            this.tags.push(tag);
        },
        del_tag(tag){
            this.tags.splice(this.tags.indexOf(tag), 1);
        },
        onKeydown(e) {
            if(e.keyCode == 13 && this.query.length > 1){
                this.add_tag(this.query);
                this.query = ""
            }
        },
        openUserDialog(index){
            this.dialog_user_index = index;
            // this.d_user = JSON.parse(JSON.stringify(user));
            if(this.dialog_user_index != -1){
                Vue.nextTick().then(function(){
                    document.getElementsByClassName('v-dialog')[0].scrollTop = 0;
                })
            }
            this.userDialog = true;
        },
        closeUserDialog(){
            this.userDialog = false;
        },
        getAllUsers(){
            axios.get('/skills/api/get_all_users_roommate/',{params: {}}).then(response => {
                this.backup_all_users = response.data.users;
                this.users = response.data.users;
                this.request_user = response.data.request_user;
                this.loaded = true;
            });
        },
        fuzzy_search(tmp_all_users, key_arr, field_query){
            if(tmp_all_users.length == 0)
                return [];
            var return_all_users = [];
            for(let i = 0;i < key_arr.length; i++){
                let result = tmp_all_users.reduce(function(map, obj) {
                    map[obj.pk] = obj[key_arr[i]];
                    return map;
                }, {});
                // map is the resulting dictionary
                let score_result = this.fuzz.extract(field_query, result, this.options);
                score_result = score_result.map(function(y){
                    return y[2];
                })
                return_all_users = return_all_users.concat(this.backup_all_users.filter(function(x){
                    return score_result.indexOf(x.pk.toString(10)) != -1;
                }));
                // console.log(key_arr[i],"---",return_all_users);
            }
            return Array.from(new Set(return_all_users));
        },
        fuzzy_search_skill(tmp_all_users, field_query){
            if (tmp_all_users.length == 0)
                return [];
            var return_all_users = [];
            for(let i = 0;i < tmp_all_users.length; i++){
                let tmp_skills = tmp_all_users[i].skills;
                let tmp_skill_arr = [];
                for (const [ key, value ] of Object.entries(tmp_skills)) {
                    tmp_skill_arr = tmp_skill_arr.concat(value);
                }
                tmp_skill_arr = tmp_skill_arr.map(function(x){
                    return x.name;
                })
                if(tmp_skill_arr.length > 0){
                    let score_result = this.fuzz.extract(field_query, tmp_skill_arr, this.options);
                    if(score_result.length > 0){
                        return_all_users[tmp_all_users[i].pk] = score_result.length;
                    }
                }
            }
            return return_all_users;
        },
        user_list_filter(tags){
            var tmp_all_users = JSON.parse(JSON.stringify(this.backup_all_users));
            var ref = this;
            tags.forEach(function(tag) {
                let colon_index = tag.indexOf(":");
                if(colon_index != -1 && colon_index != tag.length){
                    let field_tag = tag.substring(0, colon_index).toLowerCase();
                    let field_query = tag.substring(colon_index + 1).toLowerCase();
                    if(field_tag === "name"){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['first_name','last_name'], field_query);
                    }
                    else if(["role"].indexOf(field_tag) != -1){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['role'], field_query);
                    }
                    else if(["first_name", "first name", "first"].indexOf(field_tag) != -1){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['first_name'], field_query);
                    }
                    else if(["last_name", "last name", "last"].indexOf(field_tag) != -1){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['last_name'], field_query);
                    }
                    else if(["gender","sex"].indexOf(field_tag) != -1){
                        let tmp_scorer = ref.options.scorer;
                        ref.options.scorer = ref.fuzz.token_sort_ratio;
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['sex'], field_query);
                        ref.options.scorer = tmp_scorer;
                    }
                    else if(["birth date", "birth_date", "birthdate","birth","date"].indexOf(field_tag) != -1){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['birth_date'], field_query);
                    }
                    else if(["loc", "location"].indexOf(field_tag) != -1){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['location'], field_query);
                    }
                    else if(["major"].indexOf(field_tag) != -1){
                        let tmp_cutoff = ref.options.cutoff;
                        ref.options.cutoff = 70;
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['major', 'major_two', 'minor'], field_query);
                        ref.options.cutoff = tmp_cutoff;
                    }
                    else if(["year"].indexOf(field_tag) != -1){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['year'], field_query);
                    }
                    else if(["bio"].indexOf(field_tag) != -1){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['bio'], field_query);
                    }
                    else if(["email"].indexOf(field_tag) != -1){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['email'], field_query);
                    }
                    else if(["wechat"].indexOf(field_tag) != -1){
                        tmp_all_users = ref.fuzzy_search(tmp_all_users, ['wechat'], field_query);
                    }
                }
                else{
                    let tmp_kv_users = ref.fuzzy_search_skill(tmp_all_users, tag.toLowerCase());
                    let tmp_all_users_arr = []
                    for(let i = 0;i < tmp_all_users.length; i++){
                        if(tmp_all_users[i].pk in tmp_kv_users){
                            tmp_all_users[i]["tag_num"] = tmp_kv_users[tmp_all_users[i].pk];
                            tmp_all_users_arr.push(tmp_all_users[i]);
                        }
                    }
                    tmp_all_users = tmp_all_users_arr.sort(function(a,b){
                        return a.tag_num - b.tag_num;
                    });
                }
            });
            ref.users = tmp_all_users;
        },
	},
	mounted(){
        this.fuzz = require('fuzzball');
        this.options = {
            scorer: this.fuzz.partial_ratio,
            cutoff: 80,
        },
        this.getAllUsers();
	},
  };
</script>

<style scoped>
    .content-div{
        /* background-color:#fdfff9; */
        /* f0f5e5 */
        position: relative;
        /* background: url('../assets/static/css/images/cloud_new_09.jpg') no-repeat; */
        background: url('../assets/static/css/images/cloud_bg_new_02.jpg') no-repeat;
        background-attachment: fixed;
        background-position: center center;
        background-size: cover;
    }

    .top-part-wrapper{
        padding: 45px 0px 30px 0px;
        color:#000000;
        width:100%;
    }

    .checkbox-div{
        margin: 0 auto;
        width: 80%;
        max-width: 600px;
        display: flex;
        flex-flow: row wrap;
    }
    .muted-text{
        color:rgb(158, 158, 158) !important;
    }

    .title-text{
        color:#32a49a; 
        font-size:45px;
        font-weight: 500 !important;
        font-family: Times, serif !important;
    }

    .all-buttons{
        margin: 5px 0px 0px 0px;
        text-align: center;
    }

    .search-tags{
        display: flex;
        flex-flow: row wrap;
        width:80%;
        max-width: 600px;
        margin: 12px auto;
    }

    .search-tag{
        color:#32a49a;
        /* background-color: #F2B69D 70%; */
        box-shadow: 0 2px 5px 0 rgba(0,0,0,.16), 0 2px 10px 0 rgba(0,0,0,.12);
        padding: 5px 5px 5px 9px;
        border-radius: 5px;
        margin: 5px 7px 5px 0px;
    }

    .search-tag-remove{
        margin:2px 3px 1px 5px;
    }

    span.search-tag-remove:hover{
        color: #494949;
    }

    .search-form {
        /* border:1px solid #728181; */
        position: relative;
        /* top: 50%;
        left: 50%; */
        margin: 0 auto;
        width: 80%;
        max-width: 600px;
        height: 40px;
        border-radius: 5px;
        box-shadow: 0 2px 5px 0 rgba(0,0,0,.16), 0 2px 10px 0 rgba(0,0,0,.12);
        /* transform: translate(-50%, -50%); */
        background: #fff;
        transition: all 0.3s ease;
    }

    .search-icon{
        padding:12px 10px 9px 14px;
    }

    .search-input {
        position: absolute;
        top: 10px;
        left: 15px;
        font-size: 14px;
        background: none;
        color: #5a6674;
        width: 85%;
        height: 20px;
        border: none;
        appearance: none;
        outline: none;
    }

    @media (min-width: 10px) and (max-width: 767px) {
        .title-text{
            font-size:35px !important;
        }
    }

</style>