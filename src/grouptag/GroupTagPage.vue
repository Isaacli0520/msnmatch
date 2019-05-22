<template>
    <div class="container">
        <div class="col-12 mb-5" style = "width:100%; margin: 0 auto;">
            <div class="container mt-5 mb-4 text-center">
                <h1 class="display-4 skill-main-title" >Add Your Tags to Your Group</h1>
                <h6 class="text-muted">Search for existing tags or Add your own tags</h6>
            </div>
        </div>
        <div class="col-xs-12 col-sm-12 col-md-10 col-lg-8 col-xs-offset-0 col-sm-offset-0" id = "skill-list-app" style="width:100%; margin: 0 auto;">
            <div class="autocomplete mb-4" style="width:100%;">
                <div>
                    <div class="mt-2 mb-2">
                        <div class="skill-user-tags mb-3">
                            <template class="skill-user-span" v-for="(skills_of_type, skills_type_name) in skills">
                                <tag-span v-for="skill in skills_of_type"
                                    v-bind:key="skill.skill_name"
                                    v-bind:skill="skill"
                                    v-bind:clickable="'delete'"
                                    @add-skill="add_skill"
                                    @del-skill="del_skill"
                                />
                            </template>
                        </div>
                        <div class="autocomplete mt-4">
                            <div :class="['search-form', (skill_results.length>0) ? 'search-form-active': '']">
                                <div class="search-icon">
                                    <i class="fas fa-search"></i>
                                </div>
                                <input v-on:keyup="autocomplete_func" autocomplete="off" v-model="searchquery" id="myInput" type="text" name="class" placeholder="Search for a skill" class="search-input" aria-label="Search">
                            </div>
                            <div class="autocomplete-items">
                                <div class="autocomplete-item" :key="skill.skill_pk" v-for="skill in skill_results" v-on:click="add_skill(skill)" :value="skill.skill_pk">
                                    <span class="auto-main font-weight-bold" >{{ skill.skill_name }}</span>
                                    <span class="auto-tag auto-skill-type" :class="skill.skill_type">{{ skill.skill_type }}</span> 
                                    <span class="auto-tag auto-custom" v-if="skill.skill_cus">Customized</span>
                                    <span class="auto-tag auto-exist" v-if="!skill.skill_cus">Existing</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mt-4 mb-3">
                        <tag-list 
                            v-bind:all_skills="all_skills" 
                            @add-skill="add_skill"
                            @del-skill="del_skill"
                            />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import TagList from '../components/TagList'
import TagSpan from '../components/TagSpan'
import axios from 'axios'

export default{
    data: function () {
        return {
            searchquery: '',
            skill_results: [],
            skills:[],
            all_skills:{},
        }
    },
    components:{
        TagList,
        TagSpan,
    },
    computed: {
        group_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 3];
        },
    },
    methods:{
        get_all_skills(){
            axios.get('/skills/ajax/get_all_skills/',{params: {}}).then(response => {
                this.all_skills = response.data.all_skills;
            });
        },
        get_all_group_skills(){
            axios.get('/skills/ajax/get_all_group_skills/',{params: {group_pk: this.group_pk}}).then(response => {
                this.skills = response.data.all_skills;
            });
        },
        autocomplete_func(){
            if (this.searchquery.length == 0){
                this.skill_results = [];
            }
            axios.get('/skills/ajax/group_result/',{params: {searchquery: this.searchquery, group_pk: this.group_pk}}).then(response => {
                this.skill_results = [];
                this.skill_results = response.data.skill_list;
                let tmp_arr = response.data.skill_list.filter(obj =>{ return this.searchquery.toLowerCase() == obj.skill_name.toLowerCase() }); 
                if (this.searchquery.length > 0 && tmp_arr.length == 0){
                    var user_enter_skill = {
                        "skill_pk": 0,
                        "skill_name": this.searchquery,
                        "skill_intro": "",
                        "skill_type": "Custom",
                        "skill_exist": false,
                        "skill_cus":true,
                    };
                    this.skill_results.push(user_enter_skill);
                }
                });
        },
        add_skill(skill){
            axios.get('/skills/ajax/add_del_group_skill/',{params: {skill_pk: skill.skill_pk, add_del:"add", skill_cus:skill.skill_cus, skill_name:skill.skill_name, group_pk: this.group_pk}}).then(response => {
                if (skill.skill_exist == false){
                    skill.skill_exist = true;
                    if (!response.data.origin_exist){
                        this.skills[skill.skill_type].splice(this.skills[skill.skill_type].indexOf(skill), 0, skill);
                    }
                }
                });
        },
        del_skill(skill){
            axios.get('/skills/ajax/add_del_group_skill/',{params: {skill_pk: skill.skill_pk, add_del:"del", skill_name:skill.skill_name, group_pk:this.group_pk}}).then(response => {
                // console.log("delete a skill");  
                if (skill.skill_exist == true){
                    skill.skill_exist = false;
                    this.skills[skill.skill_type].splice(this.skills[skill.skill_type].indexOf(skill), 1);
                    if (skill.skill_type != "Custom"){
                        this.all_skills[skill.skill_type].push(skill);
                    }
                }
                });
        },
        },
    mounted(){
        this.get_all_group_skills();
        this.get_all_skills();
        },
    }
</script>


<style scoped lang="css">

    .autocomplete {
        width:100%;
        position: relative;
        display: inline-block;
    }

    .skill-user-tags{
        display: flex;
        flex-flow: row wrap;
        width:100%;
        margin: 5px 0px 20px 0px;
    }

    .search-form {
        position: relative;
        /* top: 50%;
        left: 50%; */
        margin: 0 auto;
        width: 100%;
        height: 40px;
        border-radius: 5px;
        /* box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);*/
        /* transform: translate(-50%, -50%); */
        box-shadow: 0 2px 5px 1px rgba(0,0,0,.16), 0 2px 10px 1px rgba(0,0,0,.12);
        background: #fff;
        transition: all 0.3s ease;
    
    }

    .search-form-active{
        border-bottom: 1px solid #ededed;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
    }
    
    .search-input {
        position: absolute;
        top: 10px;
        left: 38px;
        font-size: 14px;
        background: none;
        color: #5a6674;
        width: 85%;
        height: 20px;
        border: none;
        appearance: none;
        outline: none;
    }

    .autocomplete-items {
        position: absolute;
        z-index: 200;
        margin: 0 auto;
        width:100%;
        box-shadow: 0 2px 5px 0px rgba(0,0,0,.16), 0 2px 10px 0px rgba(0,0,0,.12);
        overflow: hidden;
        background:none;
        border-radius: 0px 0px 10px 10px;
    }

    .auto-main{
        font-size: 18px;
        font-family: Roboto,sans-serif;
    }

    .auto-tag{
        font-size: 15px !important;
        float:right;
        padding: 3px 8px 3px 8px;
        border-radius: 5px;
        margin: 0px 0px 0px 5px;
        font-family: Gill Sans, sans-serif;
        color: #ffffff;
    }

    .auto-custom{
        background-color: #e25876;
    }

    .auto-exist{
        background-color: #f2dc35;
    }

    .auto-skill-type{
        background-color: #ff5c5c;
    }

    .search-icon{
        padding:12px 10px 9px 14px;
    }

    .autocomplete-item{
        font-family: Gill Sans, sans-serif;
        width:100%;
        overflow: hidden;
        border-radius: 0px;
        padding: 10px 17px 10px 17px;
        cursor: pointer;
        background: #fff; 
    }

    div.autocomplete-item:last-child{
        border-radius: 0px 0px 10px 10px;
    }

    .autocomplete-item:hover {
        background-color: #e9e9e9; 
    }

    .Entertainment{
        background-color: #f1b9a6e7;
    }
        
    .Sport{
        background-color: #80b6e2;
    }
        
    .Game{
        background-color: #8a1ae6;
    }

    .Film{
        background-color:#4cb41b;
    }

    .Music{
        background-color:#3915db;
    }

    .General{
        background-color:#88999c;
    }

    .Language{
        background-color: #af51db;
    }

    .Books{
        background-color:#ff9900;
    }

    .Academic{
        background-color:#5bd4b6;
    }

    .Custom{
        background-color: #ff0800;
    }
</style>