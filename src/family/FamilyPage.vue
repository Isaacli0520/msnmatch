<template>
    <div class="mt-3 mb-3 col-xs-12 col-sm-12 col-md-10 col-lg-10 col-xs-offset-0 col-sm-offset-0 container" id="admin-app" style="width:100%; margin: 0 auto;">
        <div class="big-title mt-2 mb-2 text-center">
            <span>Super Cool Family Page</span>
        </div>
        <div class="card mt-3 mb-3">
            <div class="card-body">
                <div class="custom-progress" :key="family.pk" v-for="family in allFmls">
                    <div class="progress-family-title">
                        <span>{{family.group_name}}</span>
                    </div>
                    <div class="progress">
                        <div class="progress-bar bg-female" role="progressbar" :style="{width: 100*getUsersBySex(family, 'Female')/15 + '%',}" :aria-valuenow="100*getUsersBySex(family, 'Female')/15" aria-valuemin="0" aria-valuemax="100">{{getUsersBySex(family, 'Female') | prog}}</div>
                        <div class="progress-bar bg-male" role="progressbar" :style="{width: 100*getUsersBySex(family, 'Male')/15 + '%',}" :aria-valuenow="100*getUsersBySex(family, 'Male')/15" aria-valuemin="0" aria-valuemax="100">{{getUsersBySex(family, 'Male') | prog}}</div>
                        <div class="progress-bar bg-nosex" role="progressbar" :style="{width: 100*getUsersBySex(family, '')/15 + '%',}" :aria-valuenow="100*getUsersBySex(family, '')/15" aria-valuemin="0" aria-valuemax="100">{{getUsersBySex(family, '') | prog}}</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-columns">
            <family-card 
            v-for="family in allFmls"
            v-bind:family="family"
            v-bind:key="family.pk"
            @open-modal="openModal"
            />
        </div>
        <family-modal
            v-bind:family="modal_family"
            v-bind:requestUser="request_user"
            v-bind:allFmls="allFmls"
            @add-to-fav="addToFav"
            @del-from-fav="delFromFav"
        />
    </div>
</template>

<script>
import FamilyModal from '../components/FamilyModal'
import FamilyCard from '../components/FamilyCard'
import axios from 'axios'

export default {
    props:{
        },
    components: {
        FamilyModal,
        FamilyCard,
    },
    data: function(){
        return {        
        allFmls: [],  
        tags: [],
        request_user:{
                "username":"",
                "pk":"",
                "role":"",
            },
        flw_limit : 1,
        modal_family: {
            "pk": -1,
            "group_type": "",
            "group_name": "",
            "group_intro": "",
            "managers":[],
            "members":[],
            // "member_tags":[],
            "group_tags":{},
            "picture": "",
            "avatar":"",
        },
        }
    },
    computed:{
        inGroups: function(){
            return this.allFmls.filter(obj => {
                return obj.inGroup
            }).length
        },
    },
    filters: {
        prog: function (value) {
            if (value > 0){
                return value.toString(10);
            }else{
                return "";
            }
        },
    },
    methods:{
        getUsersBySex: function (family, sex) {
            if(!family.members)
                return 0;
            return family.members.filter(obj => {return obj.sex==sex}).length;
        },
        getAllFamilies(){
            axios.get('/groups/ajax/get_all_families/',{params: {}}).then(response => {
                this.allFmls = response.data.groups; 
            });
        },
        getBasicInfo(){
            axios.get('/groups/ajax/get_family_page_basic_info/', {params:{}}).then(response =>{
                let data = response.data.all_info;
                console.log("basic_info",data);
                this.request_user.role = data.request_user_role;
                this.request_user.username = data.request_user_username;
                this.request_user.pk = data.request_user_pk;
            })
        },
        openModal(family){
            this.modal_family = family;
            $('#family-modal').modal('show');
        },
        addToFav(family){
            if (this.inGroups < this.flw_limit){
                axios.get('/skills/ajax/add_to_group_list/',{params: {group_pk:family.pk}}).then(response => {
                    console.log("add to list");
                    if (response.data.success == 1){
                        console.log("sucesssssss");
                        this.getAllFamilies();
                    }
                    else{
                        alert("你来晚了亲 ( >﹏<。)～");
                    }
                    $('#family-modal').modal('hide');
                });
            }
        },
        delFromFav(family){
            axios.get('/skills/ajax/del_group_fav/',{params: {group_pk:family.pk}}).then(response => {
                this.getAllFamilies();
                $('#family-modal').modal('hide');
            });
        },
    },
    mounted(){
        this.getAllFamilies();
        this.getBasicInfo();
    },
}
</script>
    
<style scoped lang="css">
    *{
        box-sizing: border-box;
    }

    .family-instruction{
        font-family: Gill Sans, sans-serif;
    }

    .progress{
        height:22px;
    }

    .custom-progress{
        font-family: Gill Sans, sans-serif;
        margin-top:15px;
    }

    .bg-nosex{
        background-color: rgb(91, 231, 110);
    }

    .bg-male{
        background-color: rgb(27, 207, 252);
    }

    .bg-female{
        background-color: rgb(247, 115, 225);
    }

    .card-text{
        color:#000000 !important;
    }
    
    .big-title{
        color:#000000;
        font-weight: 500;
        font-size: 42px !important;
        font-family: Baskerville, "Baskerville Old Face", sans-serif;
    }

    .card-columns{
        column-count: 3 !important;
    }

    /* 
    ##Device = Most of the Smartphones Mobiles (Portrait)
    ##Screen = B/w 320px to 479px
    */

    @media (min-width: 320px) and (max-width: 480px) {
    .card-columns{
        column-count: 1 !important;
    }


    
    }

    @media (min-width: 10px) and (max-width: 319px) {
        .card-columns{
            column-count: 1 !important;
        }
    }
</style>
    
