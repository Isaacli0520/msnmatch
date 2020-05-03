<template>
    <v-app>
        <match-header></match-header>
        <v-content class="content-div">
            <v-container v-if="!loaded" fluid fill-height>
                <v-layout 
                    align-center
                    justify-center>
                    <div>
                        <v-progress-circular
                        :size="60"
                        :width="6"
                        indeterminate
                        color="teal lighten-1">
                        </v-progress-circular>
                    </div>
                </v-layout>
            </v-container>
            <v-container v-if="loaded">
                <v-row justify="center">
                    <div style="text-align: center;">
                        <h1 class="title-text">Add Your Interests</h1>
                        <h4 class="subtitle-text">Search for existing tags or add your own tags</h4>
                    </div>
                </v-row>
                <v-row justify="center">
                    <v-col cols="12" sm="12" md="8" lg="7" xl ="6"> 
                        <div class="skill-tags mb-3">
                            <template v-for="(skills_of_type, skills_type_name) in user_skills">
                                <tag-span v-for="skill in skills_of_type"
                                    :key="skill.id"
                                    :skill="skill"
                                    :clickable="'delete'"
                                    @add-skill="addSkill"
                                    @del-skill="deleteSkill"
                                />
                            </template>
                        </div>
                    </v-col>
                </v-row>
                <v-row justify="center">
                    <v-col cols="12" sm="12" md="8" lg="7" xl ="6">
                    <v-autocomplete
                        v-model="selected_item"
                        :items="search_result_items"
                        :loading="isLoading"
                        :search-input.sync="search"
                        color="black"
                        background-color="white"
                        clearable
                        solo-inverted
                        no-filter
                        hide-no-data
                        hide-selected
                        hide-details
                        placeholder="Search for Interests"
                        return-object>
                        <template v-slot:item="{ item }">
                            <v-list-item-content>
                                <v-list-item-title mb-2>{{item.name}}</v-list-item-title>
                                <v-list-item-subtitle>Type:{{item.type}}</v-list-item-subtitle>
                            </v-list-item-content>  
                        </template>
                    </v-autocomplete>
                    </v-col>
                </v-row>
                <v-row justify="center">
                    <v-col cols="12" sm="12" md="8" lg="7" xl ="6">
                        <div :key="skills_type_name" v-for="(skills_of_type, skills_type_name) in all_skills">
                            <h3 class="skill-type-text">{{skill_type_names[skills_type_name]}}</h3>
                            <div class="skill-tags">
                                <tag-span v-for="skill in skills_of_type"
                                    :key="skill.skill_pk"
                                    :skill="skill"
                                    :clickable="'add'"
                                    @add-skill="addSkill"
                                    @del-skill="deleteSkill"
                                />
                            </div>
                        </div>
                    </v-col>
                </v-row>
            </v-container>
        </v-content>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="800">
            {{success_message}}
        <v-btn color="cyan accent-1" text @click="success_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red darken-1"
            :timeout="1200">
            Sth is wrong
            <v-btn color="white" text @click="failure_snack = false"> Close </v-btn>
        </v-snackbar>
    </v-app>
</template>

<script>
import axios from 'axios'
import MatchHeader from '../components/MatchHeader'
import TagSpan from '../components/TagSpan'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
	data() {
        return {
            loaded:false,
            skillNameLimit: 40,
            selected_item:null,
            isLoading: false,
            lastTime: 0,
            entries:[],
            search: null,
            all_skills:[],
            user_skills:[],
            success_message:"",
            success_snack:false,
            failure_snack:false,
            skill_type_names: {
                "Game":"Game",
                "Academic":"Academic Interests",
                "Film and TV":"Film and TV",
                "Sport":"Sport",
                "Music":"Music",
                "Language":"Language",
                "General":"General",
                "Books":"Books",
            },
        }
	},
	components:{
        MatchHeader,
        TagSpan,
	},
	watch: {
        selected_item(val){
            if(val != null){
                this.addSkill(val);
                this.search = null;
            }
        },
        search(val) {
            if (val == null || val.length == 0){
                this.entries = [];
                this.lastTime += 1;
                return;
            }

            if (val.length < 2) return;

            this.lastTime += 1;

            this.isLoading = true
            // Lazily load input items
            axios.get('/skills/api/get_search_result/',{params: {query:val, time: this.lastTime}}).then(response => {
                if(response.data.time == this.lastTime){
                    this.entries = response.data.skills; 
                }
            })
            .catch(err => {
                console.log("error: ",err)
            })
            .finally(() => {
                if((this.entries.length > 0 && this.entries[0].name != val) || this.entries.length == 0){
                    this.entries.push({
                        id:-1,
                        name:val,
                        intro:"",
                        type:"Custom"
                    });
                }
                this.isLoading = false
            });
        },
	},
	computed:{
        search_result_items(){
            return this.entries.map(entry => {
                const skill_name = entry.name.length > this.skillNameLimit
                    ? entry.name.slice(0, this.skillNameLimit) + '...'
                    : entry.name;

                return { text:skill_name, value:this.lastTime + entry.id, id:entry.id, intro:entry.intro,name:skill_name,  type:entry.type};
            })
        },
	},
	methods: {
        getSkills(){
            axios.get('/skills/api/get_all_and_user_skills/').then(response => {
                this.all_skills = response.data.all_skills;
                this.user_skills = response.data.user_skills;
                this.loaded = true;
            });
        },
        addSkill(skill){
            axios.post("/skills/api/user_add_skill/", {
                "id":skill.id,
                "name":skill.name,
            }).then(response => {
                if(response.data.success){
                    let tmp_skill = JSON.parse(JSON.stringify(skill));
                    tmp_skill.id = response.data.id;
                    let all_skill_pos = this.all_skills[skill.type].map(function(e) { return e.id; }).indexOf(tmp_skill.id);
                    this.user_skills[tmp_skill.type].splice(-1, 0, tmp_skill);
                    if(all_skill_pos != -1)
                        this.all_skills[tmp_skill.type].splice(all_skill_pos, 1);
                    this.success_message = "Tag Added"
                    this.success_snack = true;
                }else{
                    this.failure_snack = true;
                }
            });
        },
        deleteSkill(skill){
            axios.post("/skills/api/user_del_skill/", {
                "id":skill.id,
            }).then(response => {
                if(response.data.success){
                    let user_skill_pos = this.user_skills[skill.type].map(function(e) { return e.id; }).indexOf(skill.id);
                    if(user_skill_pos != -1)
                        this.user_skills[skill.type].splice(user_skill_pos, 1);
                    if (skill.type != "Custom"){
                        this.all_skills[skill.type].push(skill);
                    }
                    this.success_message = "Tag Deleted"
                    this.success_snack = true;
                }else{
                    this.failure_snack = true;
                }
            });
        }
	},
	mounted(){
        this.getSkills();
	},
  };
</script>

<style>
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

    .skill-type-text{
        color: #32a49a;
        font-family: Palatino, URW Palladio L, serif;
    }

    .skill-tags{
        display: flex;
        flex-flow: row wrap;
        width:100%;
        margin: 5px 0px 20px 0px;
    }

    .title-text{
        color:#32a49a; 
        font-size:45px;
        font-weight: 500 !important;
        font-family: Times, serif !important;
    }

    .subtitle-text{
        font-weight: 300 !important;
        color:#a8a8a8;
        font-family: Roboto,sans-serif !important;
    }

    @media (min-width: 1025px) {
        
    }


    @media (min-width: 768px) and (max-width: 1024px) {
    }

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {

    }


    @media (min-width: 10px) and (max-width: 767px) {
        .title-text{
            font-size: 35px !important;
        }
    }


</style>