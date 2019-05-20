<template>
    <div class="mt-3 mb-3 col-xs-12 col-sm-12 col-md-10 col-lg-10 col-xs-offset-0 col-sm-offset-0 container" id="admin-app" style="width:100%; margin: 0 auto;">
        <div class="text-center mt-3 mb-3">
            <h1>Groups you can manage</h1>
        </div>
        <div class="card-columns">
            <group-card 
            v-for="group in all_manager_groups"
            v-bind:group="group"
            v-bind:key="group.pk"
            @open-modal="openModal"
            />
        </div>
        <div class="text-center mt-3 mb-3">
            <h1>Groups you are in</h1>
        </div>
        <div class="card-columns">
            <group-card 
            v-for="group in all_member_groups"
            v-bind:group="group"
            v-bind:key="group.pk"
            @open-modal="openModal"
            />
        </div>
    </div>
</template>

<script>
import GroupCard from '../components/GroupCard'
import axios from 'axios'

export default {
    props:{
        },
    components: {
        GroupCard,
    },
    data: function(){
        return {        
        all_manager_groups: [],
        all_member_groups: [],
        requestUser: {},
        modal_group: {
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
    },
    mounted(){
        axios.get('/groups/ajax/get_manager_groups/',{params: {}}).then(response => {
            this.all_manager_groups = response.data.groups; 
        });
        axios.get('/groups/ajax/get_member_groups/',{params: {}}).then(response => {
            this.all_member_groups = response.data.groups; 
        });
    },
}
</script>
    
<style scoped lang="css">
    *{
        box-sizing: border-box;
    }

    .card-columns{
        column-count: 3 !important;
    }

    @media (min-width: 481px) and (max-width: 767px) {
        .card-columns{
            column-count: 2 !important;
        }
    }

    @media (min-width: 10px) and (max-width: 480px) {
        .card-columns{
            column-count: 1 !important;
        }
    }

</style>
    
