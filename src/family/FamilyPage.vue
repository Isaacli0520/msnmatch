<template>
    <div class="mt-3 mb-3 col-xs-12 col-sm-12 col-md-10 col-lg-10 col-xs-offset-0 col-sm-offset-0 container" id="admin-app" style="width:100%; margin: 0 auto;">
        <div class="big-title mt-2 mb-2 text-center">
            <span>Super Cool Family Page</span>
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
        flw_limit : 3,
        modal_family: {
            "pk": -1,
            "group_type": "",
            "group_name": "",
            "group_intro": "",
            "managers":[],
            "members":[],
            "group_tags":{},
            "picture": "",
            "avatar":"",
        },
        }
    },
    computed:{
        following: function(){
            return this.allFmls.filter(obj => {
                return obj.follow
            }).length
        },
    },
    methods:{
        openModal(family){
            this.modal_family = family;
            $('#family-modal').modal('show');
        },
        addToFav(family){
            if (this.following >= this.flw_limit){
                    $('#follow-btn').popover({
                            trigger: 'focus',
                            placement: 'top',
                            container: 'body',
                            html: true,
                            content: "Don't be too 花心 <br /> You can only like 3 users",
                        });
                    $('#follow-btn').popover('show');
                }
            else{
                $('#follow-btn').popover('disable')
                axios.get('/skills/ajax/add_to_group_list/',{params: {group_pk:family.pk}}).then(response => {
                    $('#family-modal').modal('hide');
                    this.allFmls[this.allFmls.indexOf(family)].follow = true;
                });
            }
        },
        delFromFav(family){
            axios.get('/skills/ajax/del_group_fav/',{params: {group_pk:family.pk}}).then(response => {
                $('#follow-btn').popover('hide');
                $('#follow-btn').popover('disable');
                $('#family-modal').modal('hide');
                this.allFmls[this.allFmls.indexOf(family)].follow = false;
            });
        },
    },
    mounted(){
        axios.get('/groups/ajax/get_all_families/',{params: {}}).then(response => {
            this.allFmls = response.data.groups; 
        });
        axios.get('/groups/ajax/get_family_page_basic_info/', {params:{}}).then(response =>{
            let data = response.data.all_info;
            console.log("basic_info",data);
            this.request_user.role = data.request_user_role;
            this.request_user.username = data.request_user_username;
            this.request_user.pk = data.request_user_pk;
        })
    },
}
</script>
    
<style scoped lang="css">
    *{
        box-sizing: border-box;
    }
    
    .big-title{
        color:#32a49a;
        font-weight: 500;
        font-size: 42px !important;
        font-family: Baskerville, "Baskerville Old Face", sans-serif;
    }

    .card-columns{
        column-count: 2 !important;
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
    
