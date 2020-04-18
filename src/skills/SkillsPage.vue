<template>
    <v-app>
        <match-header></match-header>
        <v-content>
            <v-container v-if="!loaded" fluid fill-height>
                <v-autocomplete
                    v-model="selected_item"
                    :items="search_result_items"
                    :loading="isLoading"
                    :search-input.sync="search"
                    color="black"
                    background-color="grey lighten-3"
                    clearable
                    solo-inverted
                    no-filter
                    flat
                    hide-no-data
                    hide-selected
                    hide-details
                    placeholder="Search for Skills"
                    return-object>
                    <template v-slot:item="{ item }">
                        <v-list-item-content>
                            <v-list-item-title mb-2>{{item.text}}</v-list-item-title>
                            <v-list-item-subtitle v-if="item.last_taught.length > 0">Last taught:{{item.last_taught}}</v-list-item-subtitle>
                        </v-list-item-content>  
                    </template>
                </v-autocomplete>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import axios from 'axios'
import MatchHeader from '../components/MatchHeader'

  export default {
	data() {
        return {
            loaded:false,
        }
	},
	components:{
        MatchHeader,
	},
	watch: {
        selected_item(val){
            if(val != null){
                if(val.type == "course"){
                    this.goToHref("/courses/" + val.value + "/");
                }
                else if(val.type == "instructor"){
                    this.goToHref("/courses/instructors/" + val.value + "/");
                }
            }
        },
        search(val) {
            // Items have already been loaded

            if (val == null || val.length == 0){
                this.entries = [];
                this.lastTime += 1;
                return;
            }

            if (val.length < 2) return;

            this.lastTime += 1;

            // Items have already been requested
            // if (this.isLoading) return

            this.isLoading = true
            // Lazily load input items
            axios.get('/courses/ajax/course_search_result/',{params: {query:val, time: this.lastTime}}).then(response => {
                    if(response.data.time == this.lastTime){
                        this.entries = response.data.course_result; 
                    }
            })
            .catch(err => {
                console.log("error: ",err)
            })
            .finally(() => {this.isLoading = false});
        },
	},
	computed:{
	},
	methods: {
        getProfile(username){
            axios.get('/users/api/get_profile/',{params: {username:username}}).then(response => {
                if(response.data.success){
                    this.user = response.data.user;
                    this.editable = response.data.editable;
                }
                this.loaded = true;
            });
        },
	},
	mounted(){
	},
  };
</script>

<style>
    @media (min-width: 1025px) {
        
    }


    @media (min-width: 768px) and (max-width: 1024px) {
    }

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {

    }


    @media (min-width: 10px) and (max-width: 767px) {
        
    }


</style>