<template>
    <v-app>
        <v-navigation-drawer app>
            Navigation Drawer
        </v-navigation-drawer>

        <v-app-bar app>
            APP BAR
        </v-app-bar>

        <v-content>
            <v-container fluid>

            </v-container>
        </v-content>

        <v-footer app>
            Footer
        </v-footer>
    </v-app>
</template>

<script>
import axios from 'axios'

export default{
    data: function () {
        return {
            searchquery: '',
        }
    },
    components:{
    },
    methods:{
        get_all_skills(){
            axios.get('/skills/ajax/get_all_skills/',{params: {}}).then(response => {
                this.all_skills = response.data.all_skills;
            });
        },
        },
    mounted(){
        this.get_all_skills();
        },
    }
</script>


<style scoped lang="css">

    .cus-header{
        width: 100vw;
    }

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