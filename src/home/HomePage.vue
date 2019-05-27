<template>
    <div>
        <div class="modal fade" id="modal-intruction" tabindex="-1" role="dialog" aria-labelledby="modal-intruction" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modal-intruction">{{modal_title}}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div v-html="modal_content">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        <div id="wrap">
            <main>
                <div class="main">
                    <div class="col-12" style = "width:100%; margin: 0 auto;" id="header-wrapper">
                        <div id="navigation">
                            <nav class="navbar navbar-expand-md navbar-msn" >
                                <a class="navbar-brand" :href="home_url">
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
                                        <li class="nav-item">
                                            <a class="nav-link" :href="family_url">Family</a>
                                        </li>
                                        <li class="nav-item">
                                            <a class="nav-link" :href="group_manage_url">Group</a>
                                        </li>
                                    </ul>
                                </div>
                            
                                <div class="navbar-collapse collapse w-100 order-2 dual-collapse2">
                                    <ul class="navbar-nav ml-auto">
                                        <li class="nav-item dropdown">
                                            <a class="nav-link dropdown-toggle" id="help-nav" href="#" role="button" data-toggle="dropdown" aria-haspopup="true">
                                                <i class="far fa-question-circle"></i>
                                            </a>   
                                            <div class="dropdown-menu custom-drop-menu w-100 dropdown-menu-right" aria-labelledby="help-nav">
                                                <a class="dropdown-item" @click="openModal('get-started')">Get Started</a>
                                                <a class="dropdown-item" @click="openModal('match-rule')">Match Rule</a>
                                                <div class="dropdown-divider"></div>
                                                <a class="dropdown-item" @click="openModal('updates')">Updates</a>
                                            </div> 
                                        </li>
                                        <follow-list
                                        v-bind:following="following"
                                        @update-following-list="update_following_list"
                                        />
                                    <li class="nav-item dropdown">
                                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown-user" role="button" data-toggle="dropdown" aria-haspopup="true">
                                            <i class="fas fa-user"></i>
                                        </a>
                                        <div class="dropdown-menu custom-drop-menu w-100 order-4 dropdown-menu-right" aria-labelledby="navbarDropdown-user">
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
                            @update-request-user-role="update_request_user_role"
                            @user-list-filter="user_list_filter"
                            @get-users-by-sim="get_users_by_sim"
                            @update-user-list="update_user_list"/>
                        </div>
                    </div>
                    <div class="user-list-div">
                        <div style="margin: 0px 0px 35px 0px;">
                            <h3 class="line-break"><span>Hoo's My Match</span></h3>
                        </div>
                        <div v-if="!load_complete" class="lds-ring"><div></div><div></div><div></div><div></div></div>
                        <div class="col-xs-12 col-sm-12 col-md-10 col-lg-10 col-xs-offset-0 col-sm-offset-0 mb-5" style="width:100%; margin: 0 auto;">
                            <user-list
                                v-bind:allUsers="all_users"
                                v-bind:requestUser="request_user"
                                v-bind:following="following"
                                @update-following-list="update_following_list"/>
                        </div>
                    </div>
                </div>
            </main>
        </div>
        <home-footer
            v-bind:home_url="home_url"
            v-bind:tags_url="tags_url"
            v-bind:profile="profile"
        />
    </div>
</template>


<script>
    import UserList from '../components/UserList'
    import FollowList from '../components/FollowList'
    import SearchHome from '../components/SearchHome'
    import HomeFooter from '../components/HomeFooter'
    import axios from 'axios'

    export default{
        props:{
            
        },
        components:{
            UserList,
            FollowList,
            SearchHome,
            HomeFooter,
        },
        data: function (){ 
            return{
            home_url:"",
            tags_url:"",
            family_url:"",
            group_manage_url:"",
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
            modal_title:"",
            modal_title_dist:{
                "get-started":"Get Started",
                "match-rule":"Mentee Mentor Match Rule",
                "updates":"Updates",
            },
            modal_content:"",
            modal_content_dist:{
                "get-started":"<p class='font-weight-bold'>Be a Mentee or Mentor</p> \
                <p>1. Click on <strong>Be a Mentee</strong> or <strong>Be a Mentor</strong> at the home page to be a Mentee or Mentor\
                <br>2. If you don't choose a role, you won't appear in the user list at the home page and you won't be able to add anyone to your favorite list.</p>\
                <p class='font-weight-bold'>Edit Your Profile</p> \
                <p>1. Click the user dropdown menu <i class='fas fa-user'></i> and select edit profile.<br>2. <strong>Year</strong> and <strong>Major</strong> are required fields, while the others are optional.</p> \
                <p class='font-weight-bold'>Add Your Interests</p>\
                <p>1. Click on <strong>Tags</strong> at the upper-left corner to go to the Tags page.\
                <br>2. You can add skills by typing in the search bar and add existing/customized tag\
                <br>3. You can also add skills by click on the tags below the search bar\
                <br>4. To delete a tag, just click the <i class='fas fa-times'></i> of that tag</p>",

                "match-rule":"<p class='font-weight-bold'>Add to Favorite</p> \
                <p>1. Click on Mentee/Mentor Profile based on your role and you can add them to your favorte list by clicking the <strong>add to favorite</strong> button \
                <br>2. Please note that the favorite list has a preference ranking based on the order you add others to your list. \
                <br>3. The first one should be the one you prefer the most and so on for the rest.</p>\
                <p class='font-weight-bold'>How are Mentees and Mentors Matched?</p>\
                <p>1. This is done by the mentor program chair, feel free to contact him if you have any question.(WeChat Id: zgt19991026)</p>\
                ",
                
                "updates":"<p class='font-weight-bold'>2019-05-27</p> \
                <strong>1. Fuzzy search algorithm changed for specific fields</strong><br>\
                <strong>2. Number of trending tags changed from 50 to 75</strong><br>\
                <strong>3. Family page title fixed</strong><br><br>\
                <p class='font-weight-bold'>2019-05-23</p> \
                <strong>1. Add Family Page</strong> \
                <ul><li>Mentees can now like up to 3 families</li></ul>\
                <strong>2. Add Group Management Page</strong>\
                <ul><li>Family heads can now customize family information at the Group Management Page</li></ul>\
                <strong>3. Bio maximum words changed from 500 to 1000</strong>\
                "
            },
            fuzz: null,
            options:null,
            }
        },
        methods:{
            openModal(key){
                this.modal_title = this.modal_title_dist[key];
                this.modal_content = this.modal_content_dist[key];
                $('#modal-intruction').modal('show');
            },
            update_request_user_role(user_role){
                this.request_user.role = user_role;
                this.all_users.filter(obj => {
                    return obj.pk == this.request_user.pk
                })[0].role = user_role;
                this.backup_all_users.filter(obj => {
                    return obj.pk == this.request_user.pk
                })[0].role = user_role;
            },
            get_users_by_sim(){
                let req_user = this.backup_all_users.filter(obj => {
                    return obj.pk == this.request_user.pk;
                })[0];
                let other_users = this.all_users.filter(obj => {
                    return obj.pk != this.request_user.pk;
                });
                for(let i = 0; i < other_users.length; i++){
                    other_users[i]["score"] = parseFloat((this.similarity_between(req_user, other_users[i])*100).toFixed(2));
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
                        return x.skill_name;
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
                ref.all_users = tmp_all_users;
            },
            update_user_list(new_users){
                this.all_users = new_users; 
            },
            update_following_list(following_user, add_del){
                if(add_del == 1){
                    this.following.push(following_user);
                    let all_users_filtered = this.all_users.filter(function(item) { return item.pk === following_user.pk;});
                    if (all_users_filtered.length > 0)
                        all_users_filtered[0].follow = true;
                    this.backup_all_users.filter(function(item) { return item.pk === following_user.pk; })[0].follow = true;
                }
                else if(add_del == 0){
                    this.following.splice(this.following.indexOf(following_user), 1);
                    let all_users_filtered = this.all_users.filter(function(item) { return item.pk === following_user.pk;});
                    if (all_users_filtered.length > 0)
                        all_users_filtered[0].follow = false;
                    this.backup_all_users.filter(function(item) { return item.pk === following_user.pk; })[0].follow = false;
                }
            },
        },
        mounted(){
            this.fuzz = require('fuzzball');
            this.options = {
                scorer: this.fuzz.partial_ratio,
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
                this.family_url = data.family_url;
                this.group_manage_url = data.group_manage_url;
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
                this.all_users = JSON.parse(JSON.stringify(this.backup_all_users));
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
    .custom-drop-menu{
        box-shadow: 0 2px 5px 0px rgba(0,0,0,.16), 0 2px 10px 0px rgba(0,0,0,.12);
    }

    .lds-ring {
        margin: 0 auto;
        width: 80px;
        height: 80px;
        }
    .lds-ring div {
        box-sizing: border-box;
        display: block;
        position: absolute;
        width: 64px;
        height: 64px;
        margin: 8px;
        border: 8px solid #35a39a;
        border-radius: 50%;
        animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
        border-color: #35a39a transparent transparent transparent;
    }
    .lds-ring div:nth-child(1) {
        animation-delay: -0.45s;
    }
    .lds-ring div:nth-child(2) {
        animation-delay: -0.3s;
    }
    .lds-ring div:nth-child(3) {
        animation-delay: -0.15s;
    }
    @keyframes lds-ring {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }


    *{
        box-sizing: border-box;
    }
    body{
        display:flex; 
        flex-direction:column;
    }


    #wrap {
        min-height: 100%;
    }
    
    #main {
        overflow: auto;
        /* padding-bottom: 311px; */
        /* must be same height as the footer */
    }
    .user-list-div{
    /* width:100%;
    height: 100%;
    position:relative;
    background: url('images/cloud_01.jpg') no-repeat;
    background-attachment: fixed;
    background-position: center center;
    background-size: cover; */
    padding-top: 48px;
    
    }

    .line-break {
    width: 80%; 
    text-align: center; 
    border-bottom: 1px solid rgb(134, 130, 130); 
    line-height: 0.1em;
    margin: 0 auto; 
    } 

    .line-break span { 
    color:#2ea49a;
    font-weight: 350;
    font-family: Baskerville, "Baskerville Old Face", sans-serif;
    background:#fff; 
    padding:0 20px; 
    margin: 5px 0px 2px 0px;
    }

    #header-wrapper {
    position: relative;
    /* z-index: -5; */
    padding: 0px 0px 40px 0px;
    /* background-image: url("images/header.svg");
    background-image: url("images/overlay.png"), url("images/header.svg"),  -moz-linear-gradient(75deg, #FF7088 15%, #F2B69D 55%);
    background-image: url("images/overlay.png"), url("images/header.svg"), -webkit-linear-gradient(75deg, #FF7088 15%, #F2B69D 55%);
    background-image: url("images/overlay.png"), url("images/header.svg"), -ms-linear-gradient(75deg, #FF7088 15%, #F2B69D 55%);
    background-image: url("images/overlay.png"), url("images/header.svg"), linear-gradient(75deg, #FF7088 15%, #F2B69D 55%);
    background-size: 100% 180%;
    background-size: 128px 128px, 100% 180%, auto;
    background-repeat: repeat, no-repeat, no-repeat;
    background-color: #e5e2e29c;
    background-attachment: fixed;
    background-position: center center; */
    color:#000000;
    width:100%;
    /* height: 100%; */
    position:relative;
    background: url('../assets/static/css/images/cloud_new_09.jpg') no-repeat;
    background-attachment: fixed;
    background-position: center center;
    background-size: cover;

    -webkit-box-shadow: inset 0 -3px 3px 0px rgba(0,0,0,.13), inset 0 -7px 7px 0px rgba(0,0,0,.12);
    box-shadow: inset 0 -3px 3px 0px rgba(0,0,0,.13), inset 0 -7px 7px 0px rgba(0,0,0,.12);
    /* padding: 0; */
    }




    .main-title{
    margin-top: 100px;
    margin-bottom: 30px;
    color:#32a49a;
    font-weight: 800 !important;
    /* font-family: Baskerville, "Baskerville Old Face", sans-serif; */
    text-transform: uppercase;
    font-family: "Raleway", Helvetica, sans-serif;
    /* font-family: Optima, sans-serif; */
    font-size: 45px;
    letter-spacing: 0.02em;
    /* text-shadow: 1px 2px 4px rgb(155, 155, 155); */
    }

    .sub-title{
    color:#ffffff;
    }




    .loader {
    border: 16px solid #f3f3f3;
    border-radius: 50%;
    border-top: 16px solid #3498db;
    width: 100px;
    height: 100px;
    -webkit-animation: spin 2s linear infinite; /* Safari */
    animation: spin 2s linear infinite;
    margin:0 auto;
    }

    /* Safari */
    @-webkit-keyframes spin {
    0% { -webkit-transform: rotate(0deg); }
    100% { -webkit-transform: rotate(360deg); }
    }

    @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
    }




    .user-card-inner:hover .progressive-image {
    opacity: 0.3;
    transition: .5s ease;
    }


    .progressive-image {
    transition: .5s ease;
    position: relative;
    overflow: hidden;
    width: 100%;
    display: inline-block;
    
    }
    .progressive-image-canvas {
    visibility: hidden;
    position: absolute;
    top: 0;
    left: 0;
    }
    .progressive-image-main {
    border-top-left-radius: calc(.25rem - 1px);
    border-top-right-radius: calc(.25rem - 1px);
    opacity: 1;
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100%;
    height: auto;
    z-index: 1;
    transition-duration: 0.5s;
    transition-property: all;
    transition-timing-function: ease-out;
    transform: translateZ(0);
    }
    .progressive-image-before-enter {
    /* opacity: 1; */
    }
    /* .progressive-image-enter {
    opacity: 0.3;
    transition: .5s ease;
    } */
    .progressive-image-placeholder {
    position: absolute;
    top: 0px;
    left: 0px;
    z-index: 0;
    overflow: hidden;
    transition-duration: 300ms;
    transition-property: all;
    transition-timing-function: ease-out;
    backface-visibility: hidden;
    transform: translateZ(0) scale(1.1);
    width: 100%;
    height: 100%;
    background-size: cover;
    }
    .progressive-image-placeholder-out {
    transition-duration: inherit;
    transition-property: all;
    transition-timing-function: ease-out;
    /**
    * the transitioon delay needs to be longer than the
    * .progressive-image-main transition-duration, otherwise it will flick
    * because there won't be a background.
    */
    transition-delay: 0.4s;
    opacity: 0;
    }
    .progressive-image-preloader {
    pointer-events: none;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2;
    }

    #navbar-left-div ul li a {
    border-bottom: 0;
    font-family: "Raleway", Helvetica, sans-serif;
    font-size: 0.8em;
    font-weight: 320;
    letter-spacing: 0.20em;
    text-transform: uppercase;
    }

    .navbar-nav .nav-item .nav-link .fav-dropdown{
        color: rgb(255, 0, 0);
    }

    .navbar-nav .nav-item .nav-link {
    color:rgb(0, 0, 0);
    }

    .navbar-msn .navbar-toggler span {
    color:#000000;
    }

    .navbar-msn .dropdown-item {
    font-family: "Raleway", Helvetica, sans-serif;
    text-transform: uppercase;
    font-size: 13px !important;
    font-weight: 340 !important;
    letter-spacing: 0.08em !important;
    /* color: #ffffff; */
    }

    .fa-heart {
    color:#ee184d;
    }

    .navbar-msn .nav-item.active .nav-link,
    .navbar-msn .nav-item:hover .nav-link {
        color: #636363;
    }

    .navbar-msn{
    background-color: #ffffff;
    /* background:transparent; */
    }



    #navbar-left-div ul li {
        border-left: solid 1px rgba(197, 197, 197, 0.945);
        line-height: 1;
        margin-left: 1em;
        padding-left: 1em;
    }

    #navbar-left-div ul li:first-child {
    border-left: 0;
    margin-left: 0;
    padding-left: 0;
    }



    /* 
    ##Device = Desktops
    ##Screen = 1281px to higher resolution desktops
    */
    @media (min-width: 1281px) { 
    .card-columns{
        column-count: 5 !important; 
    }
    }

    /* 
    ##Device = Laptops, Desktops
    ##Screen = B/w 1025px to 1280px
    */
    @media (min-width: 1025px) and (max-width: 1280px) {
    .card-columns{
        column-count: 4 !important;
    }
    }

    /* 
    ##Device = Tablets, Ipads (portrait)
    ##Screen = B/w 768px to 1024px
    */

    @media (min-width: 768px) and (max-width: 1024px) {
    .card-columns{
        column-count: 3 !important;
    }

    .main-title{
        font-size: 45px;
    }
    }

    /* 
    ##Device = Tablets, Ipads (landscape)
    ##Screen = B/w 768px to 1024px
    */

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
    .card-columns{
        column-count: 3 !important;
    }

    .main-title{
        font-size: 36px;
    }
    }

    /* 
    ##Device = Low Resolution Tablets, Mobiles (Landscape)
    ##Screen = B/w 481px to 767px
    */

    @media (min-width: 481px) and (max-width: 767px) {
    .card-columns{
        column-count: 2 !important;
    }
    /* 
    #header-wrapper {
        position: relative;
        padding: 0px 0px 40px 0px;
        background-image: url("images/header.svg");
        background-image: url("images/overlay.png"), url("images/header.svg"),  -moz-linear-gradient(55deg, #FF7088 15%, #F2B69D 55%);
        background-image: url("images/overlay.png"), url("images/header.svg"), -webkit-linear-gradient(55deg, #FF7088 15%, #F2B69D 55%);
        background-image: url("images/overlay.png"), url("images/header.svg"), -ms-linear-gradient(55deg, #FF7088 15%, #F2B69D 55%);
        background-image: url("images/overlay.png"), url("images/header.svg"), linear-gradient(55deg, #FF7088 15%, #F2B69D 55%);
        background-color: #ffffff;
        background-size: 100% 100%;
        background-size: 128px 128px, 100% 100%, auto;
        background-repeat: repeat, no-repeat, no-repeat;
        padding: 0;
    } */

    .main-title{
        margin-top: 60px;
        margin-bottom: 30px;
        font-size: 30px;
    }

    }

    /* 
    ##Device = Most of the Smartphones Mobiles (Portrait)
    ##Screen = B/w 320px to 479px
    */

    @media (min-width: 320px) and (max-width: 480px) {
    .card-columns{
        column-count: 1 !important;
    }

    /* #header-wrapper {
        position: relative;
        padding: 0px 0px 40px 0px;
        background-image: url("images/header.svg");
        background-image: url("images/overlay.png"), url("images/header.svg"),  -moz-linear-gradient(70deg, #FF7088 15%, #F2B69D 55%);
        background-image: url("images/overlay.png"), url("images/header.svg"), -webkit-linear-gradient(70deg, #FF7088 15%, #F2B69D 55%);
        background-image: url("images/overlay.png"), url("images/header.svg"), -ms-linear-gradient(70deg, #FF7088 15%, #F2B69D 55%);
        background-image: url("images/overlay.png"), url("images/header.svg"), linear-gradient(70deg, #FF7088 15%, #F2B69D 55%);
        background-color: #ffffff;
        background-size: 100% 100%;
        background-size: 128px 128px, 100% 100%, auto;
        background-repeat: repeat, no-repeat, no-repeat;
        padding: 0;
    } */

    .main-title{
        margin-top: 60px;
        margin-bottom: 30px;
        font-size: 28px;
    }

    
    }

    @media (min-width: 10px) and (max-width: 319px) {
        .card-columns{
            column-count: 1 !important;
        }


        .main-title{
            font-size: 20px;
        }
    }
</style>