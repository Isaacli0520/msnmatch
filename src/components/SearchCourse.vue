<template>
    <v-autocomplete
        v-model="selected_item"
        :items="search_result_items"
        :loading="isLoading"
        :search-input.sync="search"
        color="black"
        :background-color="background_color"
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
</template>

<script>
import axios from 'axios';

export default {
    props:{
        background_color:{
            type:String,
            default:"grey lighten-3",
        },
    },
    data() {
        return {
            courseNameLimit: 42,
            selected_item:null,
            isLoading: false,
            lastTime: 0,
            entries:[],
            search: null,
            searchquery: '',
        }
    },
    components:{
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
            if (val.length < 2) return

            this.lastTime += 1;
            if (val == null || val.length == 0){
                this.entries = []
                return
            }

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