<template>
    <div class="mt-3 mb-3 col-xs-12 col-sm-12 col-md-10 col-lg-10 col-xs-offset-0 col-sm-offset-0 container" id="admin-app" style="width:100%; margin: 0 auto;">
        <div class="text-center mt-3 mb-3">
            <h1>Super Cool Family Page</h1>
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
            v-bind:requestUser="requestUser"
            @add-to-fav="addToFav"
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
        following: [],
        requestUser: {},
        flw_limit : 2,
        modal_family: {
            "pk": -1,
            "group_type": "",
            "group_name": "",
            "group_intro": "",
            "managers":{},
            "members":{},
            "group_tags":{},
            "picture": "",
            "avatar":"",
        },
        }
    },
    methods:{
        openModal(family){
            this.modal_family = family;
            $('#family-modal').modal('show');
        },
        addToFav(user){
            if (this.following.length >= this.flw_limit){
                    $('#follow-btn').popover({
                            trigger: 'focus',
                            placement: 'top',
                            container: 'body',
                            html: true,
                            content: "Don't be too 花心 <br /> You can only like 3 users",
                        });
                    $('#follow-btn').popover('show')
                }
            else{
                $('#follow-btn').popover('disable')
                axios.get('/skills/ajax/add_to_list/',{params: {user_pk:user.pk}}).then(response => {
                    $('#user-modal').modal('hide');
                    var tmp_fav = {
                        "pk": user.pk,
                        "user_url": user.user_url,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                    if(response.data.success == 1){
                        this.$emit('update-following-list', tmp_fav ,1); 
                    }
                });
            }
        },
    },
    mounted(){
        axios.get('/groups/ajax/get_all_families/',{params: {}}).then(response => {
            this.allFmls = response.data.groups; 
        });
    },
}
</script>
    
<style scoped lang="css">
    *{
        box-sizing: border-box;
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
    
