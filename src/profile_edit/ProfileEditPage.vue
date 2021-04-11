<template>
    <v-app>
        <match-header></match-header>
        <v-main class="content-div">
            <profile-edit 
                :username="username"
                @enable-snack="enableSnack"
                @edit-success="editSuccess"
                />
        </v-main>
        <v-snackbar
            top
            v-model="video_snack"
            color="red darken-1"
            :timeout="3200">
            Sth is wrong
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
import axios from 'axios'
import MatchHeader from '../components/MatchHeader'
import ProfileEdit from '../components/ProfileEdit'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    data() {
        return {
            failure_snack: false,
            video_snack: false,
        }
    },
    components:{
        MatchHeader,
        ProfileEdit,
    },
    computed:{
        username: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 3];
        },
    },
    methods: {
        enableSnack(snack){
            if(snack == "video_snack")
                this.video_snack = true;
            else if(snack == "failure_snack")
                this.failure_snack = true;
        },
        editSuccess(username){
            window.location.href = '/users/'+ username;
        }
    },
    mounted(){
    },
};
</script>

<style>
    .content-div{
        position: relative;
        background: url('../assets/static/css/images/cloud_bg_new_02.jpg') no-repeat;
        background-attachment: fixed;
        background-position: center center;
        background-size: cover;
    }

    .cus-table{
        table-layout: fixed;
        width:100%;
    }

    tr td:first-child{
        color: rgb(156, 154, 154);
    }

    tr td:last-child{
        color: rgb(0, 0, 0);
    }

    .left-tr{
        width:24%;
    }

    .right-td{
        width:76%;
    }

    .description-td{
        padding: 6px 16px 15px 16px !important;
        /* font-family: "Times New Roman", Times, serif !important; */
    }

    .table-title{
        font-size:20px !important;
        font-weight: 700 !important;
    }

    .v-card__title{
        font-weight: 600 !important;
    }

    .v-card__text td{
        font-family: "Times New Roman", Times, serif !important; 
        font-size: 16px !important;
        padding: 6px 16px;
    }


    td:not(.cus-td):not(.description-text){
        /* font-family: "Times New Roman", Times, serif !important;  */
        /* font-size: 15px !important; */
        /* padding: 4px 16px; */
    }

    .dialog-head-text{
        /* font-family: "Times New Roman", Times, serif !important;  */
        padding-left:31px;
        font-size: 28px !important;
        font-weight:700 !important;
    }

    @media (min-width: 1025px) {
        
    }


    @media (min-width: 768px) and (max-width: 1024px) {
    }

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {

    }


    @media (min-width: 10px) and (max-width: 767px) {
        .left-tr{
            width:28% !important;
        }

        .right-td{
            width:72% !important;
        }
        
    }


</style>