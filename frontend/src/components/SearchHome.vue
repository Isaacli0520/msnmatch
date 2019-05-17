<template>
    <div>
        <div class="search-tags mb-3">
            <span v-for="tag in tags"
                class="search-tag">
                <span>{{tag}}</span>
                <span class="search-tag-remove"><i v-on:click="del_tag(tag)" class="fas fa-times"></i></span>
            </span>
        </div>
        <div>
            <div class="search-form mt-1">
                <div class="search-icon">
                    <i class="fas fa-search"></i>
                </div>
                <input @keydown="onKeydown" v-model="searchquery" autocomplete="off" id="myInput" type="text" name="class" placeholder=" &quot;Marvel&quot;, &quot;major:Math&quot;, &quot;birth:2000&quot; " class=" search-input" aria-label="Search">
            </div>
            <div v-if="checkboxOn" class="checkbox-div">
                <div class="custom-control custom-checkbox checkboxx">
                    <input type="checkbox" class="custom-control-input" id="mentor" value="role:Mentor" v-model="tags">
                    <label class="custom-control-label role-label" for="mentor">Mentor</label>
                </div>
                <div class="custom-control custom-checkbox checkboxx">
                    <input type="checkbox" class="custom-control-input" id="mentee" value="role:Mentee" v-model="tags">
                    <label class="custom-control-label role-label" for="mentee">Mentee</label>
                </div>
            </div>
        </div>
        <div class="all-buttons">
                <button @click="getUsersBySim" class="btn btn-show-me">Best Match</button>
                <button v-if="requestUser.role == '' " @click="openModal('Mentor')" class="btn btn-show-me">Be A Mentor</button>
                <button v-if="requestUser.role == '' " @click="openModal('Mentee')" class="btn btn-show-me">Be A Mentee</button>
        </div>
        <div v-if="requestUser.role == '' " class=" mt-3 text-center">
            <small class="text-muted">*Note that you have to be a mentor/mentee to appear in the user list and perform any actions</small>
        </div>

        <div class="modal fade" id="modal_role" tabindex="-1" role="dialog" aria-labelledby="match_request" aria-hidden="true">
            <form method="post">
                {% csrf_token %}
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header text-center">
                            <h4 class="modal-title">{{modal_role}}</h4>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p class="role-confirm-text">Do you really want to be a <strong>{{modal_role}}</strong>?</p>
                            <small class="text-muted">*Note that your role can only be changed by the mentor program chair once you've made your choice.</small>
                        </div>
                        <div class="modal-footer">
                            <input type="submit" class="btn btn-primary" :name="modal_role" value="Yes">
                            <input type="button" class="btn btn-danger" data-dismiss="modal" value="No">
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>



<script>
export default {
    props:{
        'requestUser':Object,
        'checkboxOn':Boolean,
    },
    data: function(){
        return {
            searchquery: '',
            tags: [],
            modal_role:'',
            }
    },
    watch:{
        tags:function (tag){
            this.$emit('user-list-filter', this.tags)
        }
    },
    methods:{
        add_tag(tag){
            this.tags.push(tag);
        },
        del_tag(tag){
            this.tags.splice(this.tags.indexOf(tag), 1);
        },
        onKeydown(e) {
            if(e.keyCode == 13 && this.searchquery.length > 1){
                this.add_tag(this.searchquery);
                this.searchquery = ""
            }
        },
        getUsersBySim(e){
            this.$emit('get-users-by-sim');
        },
        openModal(role){
            this.modal_role = role;
            $('#modal_role').modal('show');
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
    .search-form {
        /* border:1px solid #728181; */
        position: relative;
        /* top: 50%;
        left: 50%; */
        margin: 0 auto;
        width: 80%;
        max-width: 600px;
        height: 40px;
        border-radius: 5px;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        /* transform: translate(-50%, -50%); */
        background: #fff;
        transition: all 0.3s ease;

    }

    .search-icon{
        padding:12px 10px 9px 14px;
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
    .role-label{
        color:#32a49a;
        font-family: "Raleway", Helvetica, sans-serif;
        text-transform: uppercase;
        font-size: 0.8em;
        font-weight: 380;
        letter-spacing: 0.1em;
        padding: 3px 0px 0px 0px;
    }


    .role-confirm-text{
        font-weight: 500;
        font-size:20px;
    }

    .all-buttons{
        margin: 5px 0px 0px 0px;
        text-align: center;
    }

    .search-tags{
        display: flex;
        flex-flow: row wrap;
        width:80%;
        max-width: 600px;
        margin: 0 auto;
    }

    .checkbox-div{
        margin: 0 auto;
        width: 80%;
        max-width: 600px;
        display: flex;
        flex-flow: row wrap;
    }

    .search-tag{
        color:#32a49a;
        /* background-color: #F2B69D 70%; */
        box-shadow: 0 2px 5px 0 rgba(0,0,0,.16), 0 2px 10px 0 rgba(0,0,0,.12);
        padding: 5px 5px 5px 9px;
        border-radius: 5px;
        margin: 5px 7px 5px 0px;
    }
    .search-tag-remove{
        margin:1px 3px 1px 1px;
    }

   .btn-show-me{
        /* border:solid 1px #ffffff !important; */
        border: 0 !important;
        padding: 6px 17px 6px 17px !important;
        text-transform: none !important;
        color:hsl(0, 0%, 100%) !important;
        transition: color 0.2s ease-in-out, border-color 0.2s ease-in-out, background-color 0.2s ease-in-out;
        /* background: -webkit-linear-gradient(to right, #FF7088 15%, #F2B69D);  
        background: linear-gradient(to right, #FF7088 15%, #F2B69D); */
        background-color: #32a49a !important;
        /* box-shadow: 0 6px 8px rgba(0, 0, 0, 0.295); */
        border-radius: 5px !important;
        font-family: Baskerville, "Baskerville Old Face", sans-serif;
        /* font-family: "Raleway", Helvetica, sans-serif; */
        font-weight: 300 !important;
        letter-spacing: 0.03em;
        font-size:18px !important;
        margin: 5px 5px 5px 5px;
        transition: color .3s ease-in-out,background-color .3s ease-in-out,border-color .3s ease-in-out,box-shadow .3s ease-in-out,-webkit-box-shadow .3s ease-in-out !important;       
    }

    .btn-show-me:hover {
        color: rgb(50, 164, 154) !important;
        background: #ffffff !important;
    }


    .checkboxx{
        margin: 8px 15px 8px 2px;
    } 
</style>