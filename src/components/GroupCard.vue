<template>
<div class="card group-card">
    <div class="group-card-inner">
        <div id="show-modal" @click="redirectToGroup(group.pk)">
            <progressive-img v-if="group.picture" 
                :src="group.picture" 
                :placeholder="group.avatar"
                :blur="10"
                />
        </div>
        <div class="card-body">
            <div class="title d-flex w-100 justify-content-between">
                <h5 class="mb-1 font-weight-bold">
                    {{group.group_name}}
                </h5>
                <small style="float:right;">{{ (group.members.length + group.managers.length) | pluralize }}</small>
            </div>
            <div class="group-id-tags">
                <span v-if="group.group_type" class="group-id-tag" :class="group.group_type">{{ group.group_type }}</span>
            </div>
            <small v-if="group.score && group.score > 0" class="score-text">Similarity: {{ group.score }}%</small>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import VueProgressiveImage from 'vue-progressive-image'

Vue.use(VueProgressiveImage, {})

export default {
    props: {
        group: Object,
    },
    methods: {
        openModal(modal_user){
            this.$emit('open-modal', modal_user);
        },
        redirectToGroup(group_pk){
            window.location.href = "/groups/"+ group_pk.toString(10);
        },
    },
    filters: {
        pluralize: function (value) {
            if (value > 1){
                return value.toString(10) + " Users";
            }else{
                return value.toString(10) + " User";
            }
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

    .progressive-image:hover{
        opacity: 0.45;
        transition: .5s ease;
    }

    .progressive-image {
        transition: .5s ease;
    }

    .Family{
        color:#ffffff;
        background: rgba(26, 158, 235, 0.781);
    }

    .Entertainment{
        color:#ffffff;
        background-color: #f1b9a6e7;
    }
        
    .Sport{
        color:#ffffff;
        background-color: #80b6e2;
    }
        
    .Game{
        color:#ffffff;
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
        color:#ffffff;
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
        color:#ffffff;
        background-color: #ff0800;
    }

    .group-card {
        /* margin:10px; */
        margin: 3px 3px 0.75em 3px;
        flex: 1 0 auto;
        overflow:hidden;
        /* width: 30%; */
    }

    .group-id-tags{
        margin: 0px 0px 3px 0px;
        display: flex;
        flex-flow: row wrap;
        width:100%;
    }

    .group-id-tag{
        font-size: 12px;
        font-weight: 500;
        padding: 2px 6px 2px 6px;
        margin: 5px 4px 0px 0px;
        border-radius: 4px;
    }
</style>