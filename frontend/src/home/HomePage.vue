<template>
    <div class="main">
        <div class="col-12" style = "width:100%; margin: 0 auto;" id="header-wrapper">
            <div id="navigation">
                <nav class="navbar navbar-expand-md navbar-msn" >
                    <a class="navbar-brand" href="{% url 'home' %}">
                        <img :src="brand_pic" width="30" height="30" class="d-inline-block align-top" alt="">
                    </a>
                    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target=".dual-collapse2" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <i class="fas fa-bars"></i>
                    </button>
                    <div class="navbar-collapse collapse w-100 order-1 order-md-0 dual-collapse2 " id="navbar-left-div">
                        <ul class="topBotomBordersOut navbar-nav mr-auto">
                            <li class="nav-item">
                                <a class="nav-link" :href="home_url">Home</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" :href="tags_url">Tags</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" :href="trending_tags_url">Trending Tags</a>
                            </li>
                        </ul>
                    </div>
                
                    <div class="navbar-collapse collapse w-100 order-2 dual-collapse2">
                        <ul class="navbar-nav ml-auto">
                            <follow-list
                            v-bind:following="following"
                            @update-following-list="update_following_list"
                            />
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true">
                                <i class="fas fa-user"></i>
                            </a>
                            <div class="dropdown-menu w-100 order-4 dropdown-menu-right" aria-labelledby="navbarDropdown">
                                <a class="dropdown-item" :href="profile">Profile</a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item" :href="update_profile">Edit Profile</a>
                                <a class="dropdown-item" :href="logout">Log out</a>
                            </div>
                        </li>
                        </ul>
                    </div>
                </nav>
            </div>
            <div class="container mb-1 text-center">
                <h1 class="main-title">MSN Mentor-Mentee Match</h1>
            </div>
            <div class="tag mb-3" style="width:100%;">
                <search-home
                v-bind:checkboxOn="load_complete"
                v-bind:requestUser="request_user" 
                @user-list-filter="user_list_filter"
                @get-users-by-sim="get_users_by_sim"
                @update-user-list="update_user_list"/>
            </div>
        </div>
        <div class="user-list-div">
            <div style="margin: 0px 0px 35px 0px;">
                <h3 class="line-break"><span>Hoo's My Match</span></h3>
            </div>
            <div v-if="!load_complete" class="loader"></div>
            <div class="col-xs-12 col-sm-12 col-md-10 col-lg-10 col-xs-offset-0 col-sm-offset-0 mb-5" style="width:100%; margin: 0 auto;">
                <user-list
                    v-bind:allUsers="all_users"
                    v-bind:requestUser="request_user"
                    v-bind:following="following"
                    @update-following-list="update_following_list"/>
            </div>
        </div>
    </div>
</template>


<script>
    import UserList from '../components/UserList'
    import FollowList from '../components/FollowList'
    import SearchHome from '../components/SearchHome'
    import axios from 'axios'

    export default{
        props:{
            
        },
        components:{
            UserList,
            FollowList,
            SearchHome,
        },
        data: function (){ 
            return{
            home_url:"",
            tags_url:"",
            trending_tags_url:"",
            brand_pic:"",
            profile:"",
            update_profile:"",
            logout:"",
            backup_all_users:[],
            all_users:[],
            following:[],
            load_complete: false,
            request_user:{
                "username":"",
                "pk":"",
                "role":"",
            },
            fuzz: null,
            options:null,
            }
        },
        methods:{
            get_users_by_sim(){
                let req_user = this.backup_all_users.filter(obj => {
                    return obj.pk == this.request_user.pk;
                })[0];
                let other_users = this.all_users.filter(obj => {
                    return obj.pk != this.request_user.pk;
                });
                for(let i = 0; i < other_users.length; i++){
                    other_users[i]["score"] = (this.similarity_between(req_user, other_users[i])*100).toFixed(2);
                }
                this.all_users = other_users.sort(function(a,b){
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
                        let a_tmp_names = value.map(obj => { return obj.skill_name });
                        let b_tmp_names = b_skills[key].map(obj => { return obj.skill_name });
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
                    console.log("what the f*** are you doing?(Cosine)");
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
            fuzzy_search(tmp_all_users, key_arr, field_query){
                var return_all_users = [];
                for(let i = 0;i < key_arr.length; i++){
                    let result = tmp_all_users.reduce(function(map, obj) {
                        map[obj.pk] = obj[key_arr[i]];
                        return map;
                    }, {});
                    let score_result = fuzz.extract(field_query, result, this.options);
                    score_result = score_result.map(function(y){
                        return y[2];
                    })
                    return_all_users = return_all_users.concat(this.backup_all_users.filter(function(x){
                        return score_result.indexOf(x.pk.toString(10)) != -1;
                    }));
                }
                return Array.from(new Set(return_all_users));
            },
            fuzzy_search_skill(tmp_all_users, field_query){
                var return_all_users = [];
                for(let i = 0;i < tmp_all_users.length; i++){
                    let tmp_skills = tmp_all_users[i].skills;
                    let tmp_skill_arr = [];
                    for (const [ key, value ] of Object.entries(tmp_skills)) {
                        tmp_skill_arr = tmp_skill_arr.concat(value);
                    }
                    tmp_skill_arr = tmp_skill_arr.map(function(x){
                        return x.skill_name;
                    })
                    if(tmp_skill_arr.length > 0){
                        let score_result = fuzz.extract(field_query, tmp_skill_arr, this.options);
                        if(score_result.length > 0){
                            return_all_users[tmp_all_users[i].pk] = score_result.length;
                        }
                    }
                }
                return return_all_users;
            },
            user_list_filter(tags){
                var tmp_all_users = this.backup_all_users;
                var ref = this;
                tags.forEach(function(tag) {
                    colon_index = tag.indexOf(":");
                    if(colon_index != -1 && colon_index != tag.length){
                        field_tag = tag.substring(0, colon_index).toLowerCase();
                        field_query = tag.substring(colon_index + 1).toLowerCase();
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
                            tmp_all_users = ref.fuzzy_search(tmp_all_users, ['sex'], field_query);
                        }
                        else if(["birth date", "birth_date", "birthdate","birth","date"].indexOf(field_tag) != -1){
                            tmp_all_users = ref.fuzzy_search(tmp_all_users, ['birth_date'], field_query);
                        }
                        else if(["loc", "location"].indexOf(field_tag) != -1){
                            tmp_all_users = ref.fuzzy_search(tmp_all_users, ['location'], field_query);
                        }
                        else if(["major"].indexOf(field_tag) != -1){
                            let tmp_cutoff = ref.options.cutoff;
                            ref.options.cutoff = 40;
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
                        tmp_kv_users = ref.fuzzy_search_skill(tmp_all_users, tag.toLowerCase());
                        tmp_all_users_arr = []
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
                ref.update_user_list(tmp_all_users);
            },
            update_user_list(new_users){
                this.all_users = new_users; 
            },
            update_following_list(following_user, add_del){
                if(add_del == 1){
                    this.following.push(following_user)
                    this.all_users.filter(function(item) { return item.pk === following_user.pk; })[0].follow = true;
                }
                else if(add_del == 0){
                    this.following.splice(this.following.indexOf(following_user), 1);
                    this.all_users.filter(function(item) { return item.pk === following_user.pk; })[0].follow = false;
                }
            },
        },
        mounted(){
            this.fuzz = require('fuzzball');
            this.options = {
                scorer: this.fuzz.token_set_ratio,
                cutoff: 80,
            },
            this.request_user.username = this.request_user_username;
            this.request_user.role = this.request_user_role;
            this.request_user.pk = this.request_user_pk;
            axios.get('/ajax/get_home_page_basic_info/',{params: {}}).then(response => {
                // console.log(response.data.all_users);
                let data = response.data.all_info;
                this.home_url = data.home_url;
                this.tags_url = data.tags_url;
                this.trending_tags_url = data.trending_tags_url;
                this.brand_pic = data.brand_pic;
                this.profile = data.profile;
                this.update_profile = data.update_profile;
                this.logout = data.logout;
                this.request_user.username = data.request_user_username;
                this.request_user.pk = data.request_user_pk;
                this.request_user.role = data.request_user_role;
            });
            axios.get('/skills/ajax/get_all_users/',{params: {}}).then(response => {
                // console.log(response.data.all_users);
                this.backup_all_users = response.data.all_users;
                this.all_users = this.backup_all_users;
                this.load_complete = true;
            });

            axios.get('/skills/ajax/get_follow_list/',{params: {}}).then(response => {
                // console.log("get update users", response.data.following);
                this.following = response.data.following;
            });
        },
    }
</script>

<style lang="css">
    *{
        box-sizing: border-box;
    }
</style>