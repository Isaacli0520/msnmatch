<template>
    <div>
        <div class="card-columns">
            <user-card 
            v-if="user.role != '' " 
            v-for="user in allUsers"
            v-bind:user="user"
            @open-modal="openModal"
            />
        </div>
        <user-modal
            v-bind:user="modal_user"
            v-bind:requestUser="requestUser"
            @add-to-fav="addToFav"
        />
    </div>
</template>

<script>
import UserModal from './UserModal'
import UserCard from './UserCard'
import axios from 'axios'

export default {
    props:{
        "allUsers": Array,
        "requestUser": Object,
        "following": Array,
        },
    components: {
        UserModal,
        UserCard,
    },
    data: function(){
        return {          
        tags: [],
        flw_limit : 3,
        modal_user: {
            "pk": "",
            "user_url": "",
            "picture": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "bio": "",
            "birth_date": "",
            "location": "",
            "year": "",
            "major": "",
            "skills":"",
            "video":"",
        },
        }
    },
    methods:{
        openModal(user){
            this.modal_user = user;
            $('#user-modal').modal('show');
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
                    $('#userProfileModal').modal('hide');
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
        
    },
}
</script>
    
<style scoped lang="css">
    *{
        box-sizing: border-box;
    }
</style>
    
