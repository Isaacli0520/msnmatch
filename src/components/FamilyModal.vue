<template>
    <div class="modal fade" id="family-modal" tabindex="-1" role="dialog" aria-labelledby="family-modal-label" aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="family-modal-label">{{ family.group_name }}</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <img :src="family.picture" class="card-img-top" alt="None">
                    <div class="skill-tags">
                        <template v-for="(skills_of_type, skills_type_name) in family.group_tags">
                            <tag-span v-for="skill in skills_of_type"
                                v-bind:key="skill.skill_pk"
                                v-bind:skill="skill"
                                v-bind:clickable="'href'"
                            />
                        </template>
                    </div>
                    <table class="table table-user-information">
                        <tbody>
                            <tr>
                                <td class="field-title">Family Heads</td>
                                <td class="inline-names"><a :href="tmp_user.user_url" class="inline-name inline-manager" :key="tmp_user.pk" v-for="tmp_user in family.managers"><span>{{ tmp_user.first_name }} {{ tmp_user.last_name }}</span></a></td>
                            </tr>
                            <tr>
                                <td class="field-title">Family Members</td>
                                <td class="inline-names"><a :href="tmp_user.user_url" class="inline-name inline-member" :key="tmp_user.pk" v-for="tmp_user in family.members"><span>{{ tmp_user.first_name }} {{ tmp_user.last_name }}</span></a></td>
                            </tr>
                            <tr>
                                <td class="field-title">Family Name</td>
                                <td>{{family.group_name}}</td>
                            </tr>
                            <tr>
                                <td class="field-title">Family Intro</td>
                                <td>{{family.group_intro}}</td>
                            </tr>
                            
                            
                        </tbody>
                    </table>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" id="follow-btn"
                            class="btn btn-Primary" 
                            v-if="inGroups == 0 && !family.inGroup && requestUser.role == 'Mentee' && (family.managers.map(obj => {return obj.pk;}).indexOf(requestUser.pk) == -1)"
                            @click.stop="addToFav(family)"
                            >Add to Favorites</button>
                        <button type="button" id="unfollow-btn"
                            class="btn btn-Danger" 
                            v-if="family.inGroup && requestUser.role == 'Mentee'  && (family.managers.map(obj => {return obj.pk;}).indexOf(requestUser.pk) == -1)"
                            @click.stop="delFromFav(family)"
                            >Remove from Favorites</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>

import TagSpan from './TagSpan'
export default {
    props: {
        requestUser: Object,
        family: Object,
        allFmls: Array,
    },
    components: {
        TagSpan,
    },
    methods: {
        addToFav(family){
            this.$emit('add-to-fav', family); 
        },
        delFromFav(family){
            this.$emit('del-from-fav', family); 
        },
    },
    computed:{
        inGroups: function(){
            return this.allFmls.filter(obj => {
                return obj.inGroup
            }).length
        },
    },
    mounted(){
        console.log("mounted", this.manager_pk);
    },
}
</script>

<style scoped lang="css">
    *{
        box-sizing: border-box;
    }

    td{
        word-wrap:break-word;
        white-space: pre-line;
    }
    .skill-tags{
        display: flex;
        flex-flow: row wrap;
        width:100%;
        margin: 5px 0px 20px 0px;
        }

    .inline-names{
        display: flex;
        flex-flow: row wrap;
        }

    .inline-name{
        padding: 5px 9px 5px 9px;
        border-radius: 5px;
        margin: 3px 4px 3px 0px;
        font-family: Gill Sans, sans-serif;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.175);
        color: #ffffff;
    }

    .inline-manager{
        background-color: #5bd4b6;
    }

    .inline-member{
        background-color: #e23b8e;
    }

    .skill-tag{
        padding: 5px 9px 5px 9px;
        border-radius: 5px;
        margin: 5px 4px 5px 0px;
        font-family: Gill Sans, sans-serif;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.175);
    }
    .field-title{
        font-weight: 670;
        width:20%;
    }

    .table-user-information{
        table-layout: fixed;
    }

    .modal-body{
        padding: 16px 16px 0px 16px;
    }

.Entertainment{
    color: #ffffff;
    background-color: #f1b9a6e7;
}
      
.Sport{
    color: #ffffff;
    background-color: #80b6e2;
}
    
.Game{
    color: #ffffff;
    background-color: #8a1ae6;
}

.Film{
    color:#ffffff;
    background-color:#4cb41b;
}

.Music{
    color:#ffffff;
    background-color:#3915db;
}

.General{
    color:#ffffff;
    background-color:#88999c;
}

.Language{
    color: #ffffff;
    background-color: #af51db;
  }

.Books{
    color:#ffffff;
    background-color:#ff9900;
}

.Academic{
    color:#ffffff;
    background-color:#5bd4b6;
}

.Custom{
    color: #ffffff;
    background-color: #ff0800;
}
</style>