<template>
    <v-app>
        <match-header
            @del-from-fav="deleteFromFav"
            :headerUpdate="headerUpdate"></match-header>
        <v-main class="content-div">
            <v-container class="fill-height" v-if="!loaded">
                <v-row justify="center" align="center">
                    <v-progress-circular
                        :size="60"
                        :width="6"
                        indeterminate
                        color="teal lighten-1"/>
                </v-row>
            </v-container>
            <v-container v-else>
                <div class="top-part-wrapper">
                    <v-row justify="center">
                        <div style="text-align: center;">
                            <h1 class="title-text">Mentee-Mentor Match</h1>
                            <!-- <h4 class="subtitle-text">Search for existing tags or add your own tags</h4> -->
                        </div>
                    </v-row>
                    <v-row>
                        <div class="search-tags mb-3">
                            <span :key="index" v-for="(tag,index) in tags"
                                class="search-tag">
                                <span>{{tag}}</span>
                                <span class="search-tag-remove">
                                    <v-icon color="teal lighten-2" style="margin-bottom:2px;" small @click="del_tag(tag)">mdi-close-thick</v-icon>
                                </span>
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
                                class="search-input" 
                                aria-label="Search">
                        </div>
                    </v-row>
                    <v-row>
                        <div class="checkbox-div">
                            <v-checkbox v-model="tags" hide-details class="mx-2" value="role:Mentor" label="Mentor"></v-checkbox>
                            <v-checkbox v-model="tags" hide-details class="mx-2" value="role:Mentee" label="Mentee"></v-checkbox>
                        </div>
                    </v-row>
                    <v-row justify="center" v-if="request_user.role == '' ">
                        <div style="text-align:center; margin-top:13px;">
                            <v-btn style="margin-right: 10px;" outlined color="teal lighten-1" @click="openRoleDialog('Mentor')">Be A Mentor</v-btn>
                            <v-btn outlined color="teal lighten-1" @click="openRoleDialog('Mentee')">Be A Mentee</v-btn>
                        </div>
                    </v-row>
                    <v-row justify="center" v-if="request_user.role != '' ">
                        <div style="text-align:center; margin-top:13px;">
                            <v-btn outlined color="teal lighten-1" @click="get_users_by_sim();clicked=true;">Click Me!</v-btn>
                        </div>
                    </v-row>
                    <v-row justify="center" style="margin-top:7px;">
                        <div v-if="clicked" style="text-align:center;">
                            <small class="muted-text">*这就是个随便写的算法大家开心就好😁</small>
                        </div>
                    </v-row>
                    <v-row justify="center">
                        <div v-if="clicked" style="text-align:center;">
                            <small class="muted-text">*以及你至少需要有一个tag</small>
                        </div>
                    </v-row>
                    <v-row justify="center">
                        <div v-if="request_user.role == '' " style="text-align:center;">
                            <small class="muted-text">*Note that you have to be a mentor/mentee to appear in the user list</small>
                        </div>
                    </v-row>
                </div>
                <!-- <v-divider style="margin-left:13px;margin-right:13px;"></v-divider> -->
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
                            :user_index="i"
                            :user="user" @open-user-dialog="openUserDialog"></user-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
        <user-dialog
            v-if="d_user"
            :add_to_fav="request_user.role!='' && request_user.role != d_user.role"
            :edit="request_user.username == d_user.username"
            :user="d_user"
            @add-to-fav="addToFav"
            @del-from-fav="deleteFromFav"
            v-model="userDialog"></user-dialog>
        <v-dialog v-if="loaded" v-model="roleDialog" scrollable min-width="350px" max-width="800px">
            <v-stepper v-model="current_step">
                <v-stepper-header>
                    <v-stepper-step :complete="current_step > 1" step="1">
                        Basic Info
                    </v-stepper-step>
                    <v-stepper-step :complete="current_step > 2" step="2">
                        Add Tags
                    </v-stepper-step>
                    <v-stepper-step :complete="current_step > 3" step="3">
                        Be a Mentor!
                    </v-stepper-step>
                </v-stepper-header>
                <v-stepper-items>
                    <v-stepper-content step="1">
                        <v-card class="stepper-card" height="450px">
                            <profile-edit :username="request_user.username" @edit-success="editSuccess" @enable-snack="enableSnack" />
                        </v-card>
                        <v-btn color="primary" @click="current_step=2">Continue</v-btn>
                    </v-stepper-content>
                    <v-stepper-content step="2">
                        <v-card class="stepper-card" height="450px">

                        </v-card>
                        <v-btn color="primary" @click="current_step=3">Continue</v-btn>
                    </v-stepper-content>
                    <v-stepper-content step="3">
                        <v-card class="stepper-card" height="450px">

                        </v-card>
                        <v-btn color="primary" @click="current_step=1">Continue</v-btn>
                    </v-stepper-content>
                </v-stepper-items>
            </v-stepper>
        </v-dialog>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="1800">
            {{success_text}}
            <template v-slot:action="{ attrs }">
                <v-btn color="cyan accent-1" v-bind="attrs" text @click="success_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red lighten-1"
            :timeout="2700">
            {{failure_text}}
            <template v-slot:action="{ attrs }">
                <v-btn color="white" v-bind="attrs" text @click="failure_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
        <v-snackbar
            top
            v-model="video_snack"
            color="purple lighten-1"
            :timeout="3200">
            Video may take longer to upload. Be patient :)
            <template v-slot:action="{ attrs }">
                <v-btn color="white" v-bind="attrs" text @click="video_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
    </v-app>
</template>

<script>
import Vue from "vue";
import axios from 'axios'
import MatchHeader from '../components/MatchHeader'
import UserDialog from '../components/UserDialog'
import UserCard from '../components/UserCard'
import ProfileEdit from '../components/ProfileEdit'
// import { MatchHeader, UserDialog, UserCard } from "../components"
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    data() {
        return {
            loaded:false,
            clicked:false,
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
            video_snack:false,
            // Stepper
            current_step:1,
        }
    },
    components:{
        MatchHeader,
        UserCard,
        UserDialog,
        ProfileEdit,
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
        enableSnack(snack){
            if(snack == "video_snack")
                this.video_snack = true;
            else if(snack == "failure_snack"){
                this.failure_text = "Sth is wrong";
                this.failure_snack = true;
            }
        },
        editSuccess(){
            this.current_step = 2;
        },
        addToFav(user){
            this.changeFav(user, true);
        },
        deleteFromFav(user){
            this.changeFav(user, false);
        },
        changeFav(user, boolVal){
            for(let i = 0;i < this.users.length;i++){
                if(this.users[i].pk == user.pk){
                    this.users[i].follow = boolVal;
                }
            }
            for(let i = 0;i < this.backup_all_users.length;i++){
                if(this.backup_all_users[i].pk == user.pk){
                    this.backup_all_users[i].follow = boolVal;
                }
            }
            this.headerUpdate = !this.headerUpdate;
        },
        setRole(role){
            this.roleBtnLoading = true;
            axios.post('/users/api/choose_role/',{"role":role}).then(response => {
                this.roleDialog = false;
                this.roleBtnLoading = false;
                if(response.data.success){
                    this.success_text = "恭喜你成为" + role + "!";
                    this.success_snack = true;
                    this.headerUpdate = !this.headerUpdate;
                    this.getAllUsers();
                }
                else if(response.data.message == "You don't have enough course comments."){
                    this.failure_text = "你大概是没填够三条大于15字的HoosMyProfessor课程评价";
                    this.failure_snack = true;
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
            axios.get('/users/api/get_all_users/',{params: {}}).then(response => {
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
        get_users_by_sim(){
            let req_user = this.backup_all_users.filter(obj => {
                return obj.pk == this.request_user.pk;
            })[0];
            let other_users = this.users.filter(obj => {
                return obj.pk != this.request_user.pk;
            });
            for(let i = 0; i < other_users.length; i++){
                other_users[i]["score"] = parseFloat((this.similarity_between(req_user, other_users[i])*100).toFixed(2));
            }
            this.users = other_users.sort(function(a,b){
                return b.score - a.score;
            });
        },
        similarity_between(a, b){
            if (!("skills" in a) || !("skills" in b)){
                return 0;
            }
            let a_skills = a.skills;
            let b_skills = b.skills;
            let total_length = 0;
            let a_length = 0;
            let b_length = 0;
            let sims = [];
            for (const [ key, value ] of Object.entries(a_skills)) {
                total_length += this.scaler(value.length);
                a_length += value.length;
            }
            for (const [ key, value ] of Object.entries(b_skills)) {
                b_length += value.length;
            }
            for (const [ key, value ] of Object.entries(a_skills)) {
                if(key in b_skills){
                    let a_tmp_names = value.map(obj => { return obj.name });
                    let b_tmp_names = b_skills[key].map(obj => { return obj.name });
                    let tmp_skill_list = Array.from(new Set(a_tmp_names.concat(b_tmp_names)));
                    let a_vec = tmp_skill_list.map( obj =>{
                        return a_tmp_names.indexOf(obj) != -1 ? 1 : 0;
                    })
                    let b_vec = tmp_skill_list.map( obj =>{
                        return b_tmp_names.indexOf(obj) != -1 ? 1 : 0;
                    })
                    let cosine_scaler = 1-(Math.abs(value.length/a_length - b_skills[key].length/b_length) + Math.abs(value.length - b_skills[key].length)/tmp_skill_list.length)/2;
                    sims.push(this.cosine_sim(a_vec, b_vec) * (cosine_scaler) * this.scaler(value.length)/total_length);
                }
            }
            return sims.reduce(function(a,b){ return a + b; }, 0);
        },
        cosine_sim(u,v){
            if(u.length != v.length){
                // console.log("what the f*** are you doing?(Cosine)");
                return 0;
            }
            let uv = 0;
            let u_len = 0;
            let v_len = 0;
            for(let i = 0; i < u.length;i++){
                uv += u[i]*v[i];
                u_len += u[i]*u[i];
                v_len += v[i]*v[i]
            }
            return uv/Math.sqrt(u_len)/Math.sqrt(v_len);
        },
        scaler(x){
            return Math.pow((x+1),(2/3.0))-Math.pow((x+1),(-1/8.0));
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
    .stepper-card{
        margin-bottom: 6px;
        overflow: scroll;
    }

    .content-div{
        position: relative;
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
        margin:0px 1px 0px 4px;
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

    @media (min-width: 1025px) {
        
    }


    @media (min-width: 768px) and (max-width: 1024px) {
        
    }

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
        
    }


    @media (min-width: 10px) and (max-width: 767px) {
        .title-text{
            font-size:35px !important;
        }
    }

</style>