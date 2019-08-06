<template>
    <v-app>
        <custom-header></custom-header>
        <v-content>
            <v-container fluid grid-list-lg>
                <v-layout row>
                    <v-flex xs12 sm12 md12 lg12 xl12>
                        <v-card>
                            <v-card-title>
                                Add Course Instructor
                            </v-card-title>
                            <v-card-text>
                                <v-layout row wrap>
                                    <v-flex d-flex child-flex>
                                        <v-select
                                            v-model="semester"
                                            :items="semesters"
                                            item-text="text"
                                            item-value="text"
                                            label="Semester"
                                            :menu-props="{ offsetY: true }"
                                            outlined>
                                        </v-select>
                                    </v-flex>
                                    <v-flex xs12 sm12 md6 lg6 xl6>
                                        <v-autocomplete
                                            v-model="selected_item"
                                            :items="search_result_items"
                                            :loading="isLoading"
                                            :search-input.sync="search"
                                            color="teal"
                                            clearable
                                            solo-inverted
                                            no-filter
                                            flat
                                            hide-no-data
                                            hide-selected
                                            hide-details
                                            placeholder="Search for Courses/Instructors"
                                            return-object>
                                            <template v-slot:item="{ item }">
                                                <v-list-item-content>
                                                    <v-list-item-title mb-2>{{item.text}}</v-list-item-title>
                                                    <v-list-item-subtitle v-if="item.last_taught.length > 0">Last taught:{{item.last_taught}}</v-list-item-subtitle>
                                                </v-list-item-content>  
                                            </template>
                                        </v-autocomplete>
                                    </v-flex>
                                </v-layout>
                            </v-card-text>
                        </v-card>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'

  export default {
    data() {
        return {
            semester:"2016Fall",
            courseNameLimit: 42,
            selected_item:null,
            isLoading: false,
            lastTime: 0,
            entries:[],
            search: null,
            semesters:[
                {
                    "text":"2016Fall",
                },
                {
                    "text":"2017Spring",
                },
                {
                    "text":"2017Fall",
                },
                {
                    "text":"2018Spring",
                },
                {
                    "text":"2018Fall",
                },
                {
                    "text":"2019Spring",
                },
                {
                    "text":"2019Fall",
                },
                {
                    "text":"2020Spring",
                },
            ],
        }
    },
    components:{
        CustomHeader,
    },
    watch:{
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
            this.entries = []
            return
            }
            if (val.length < 2) return

            // Items have already been requested
            // if (this.isLoading) return

            this.isLoading = true
            this.lastTime += 1;
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
        search_result_items(){
            return this.entries.map(entry => {
                if(entry.type == "course"){
                    let tmp_course_name = entry.mnemonic + entry.number + " " + entry.title;
                    const course_name = tmp_course_name.length > this.courseNameLimit
                        ? tmp_course_name.slice(0, this.courseNameLimit) + '...'
                        : tmp_course_name;

                    return {text:course_name, value:entry.pk, last_taught:entry.last_taught, type:"course"};
                }
                else if(entry.type == "instructor"){
                    return {text:entry.name, value:entry.pk,  last_taught:entry.last_taught, type:"instructor"};
                }
                else{
                    console.log("Search Bar Error");
                    return {}
                }
                })
        },
    },
    methods: {
        goToHref(href){
            window.location.href = href;
        },
    },
    mounted(){
    },
  };
</script>

<style>
  
</style>