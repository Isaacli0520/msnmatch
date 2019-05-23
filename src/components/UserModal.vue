<template>
    <div class="modal fade" id="user-modal" tabindex="-1" role="dialog" aria-labelledby="user-modal-label" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="user-modal-label">{{user.first_name}} {{user.last_name}}</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <img :src="user.picture" class="card-img-top" alt="None">
                <div class="skill-tags">
                    <template v-for="(skills_of_type, skills_type_name) in user.skills">
                        <tag-span v-for="skill in skills_of_type"
                            v-bind:key="skill.skill_pk"
                            v-bind:skill="skill"
                            v-bind:clickable="'href'"
                        />
                    </template>
                </div>
                <div>
                    <table class="table table-user-information">
                        <tbody>
                            <tr>
                                <td class="field-title">Email</td>
                                <td>{{user.email}}</td>
                            </tr>
                            <tr>
                                <td class="field-title">Year</td>
                                <td>{{user.year}}</td>
                            </tr>
                            <tr v-if="user.major">
                                <td class="field-title">Major</td>
                                <td>{{user.major}}</td>
                            </tr>
                            <tr v-if="user.major_two">
                                <td class="field-title">Second Major</td>
                                <td>{{user.major_two}}</td>
                            </tr>
                            <tr v-if="user.minor">
                                <td class="field-title">Minor</td>
                                <td>{{user.minor}}</td>
                            </tr>
                            <tr v-if="user.role">
                                <td class="field-title">Role</td>
                                <td>{{user.role}}</td>
                            </tr>
                            <tr v-if="user.wechat">
                                <td class="field-title">WeChat ID</td>
                                <td>{{user.wechat}}</td>
                            </tr>
                            <tr v-if="user.birth_date">
                                <td class="field-title">Birth Date</td>
                                <td>{{user.birth_date}}</td>
                            </tr>
                            <tr v-if="user.sex">
                                <td class="field-title">Gender</td>
                                <td>{{user.sex}}</td>
                            </tr>
                            <tr v-if="user.location">
                                <td class="field-title">Location</td>
                                <td>{{user.location}}</td>
                            </tr>
                            <tr v-if="user.bio">
                                <td class="field-title">Bio</td>
                                <td>{{user.bio}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                    <div v-if="user.video.length">
                        <video width="100%" controls :src="user.video">
                            Your Browser does not support video tags lol
                        </video>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" id="follow-btn" v-if="requestUser.role != '' 
                    && user.role != ''
                    && !user.follow 
                    && user.role != requestUser.role 
                    && requestUser.pk != user.pk " 
                    class="btn btn-Primary" @click.stop="addToFav(user)"
                    >Add to Favorites</button>
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
        user: Object,
    },
    components: {
        TagSpan,
    },
    methods: {
        addToFav(modal_user){
            this.$emit('add-to-fav', modal_user); 
        },
    },
    computed: {
    }
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

    .skill-tag{
        padding: 5px 9px 5px 9px;
        border-radius: 5px;
        margin: 5px 4px 5px 0px;
        font-family: Gill Sans, sans-serif;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.175);
    }
    .field-title{
        font-weight: 670;
        width:30%;
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