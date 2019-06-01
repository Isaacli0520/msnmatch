<template>
<div class="card group-card">
    <div class="group-card-inner">
        <div id="show-modal" @click="openModal(family)">
            <progressive-img v-if="family.picture" 
                :src="family.picture" 
                :placeholder="family.avatar"
                :blur="10"
                />
        </div>
        <div class="card-body">
            <div class="d-flex w-100 justify-content-between">
                <h4 class="mb-1">
                    {{ family.group_name }}
                </h4>
            </div>
            <div class="group-id-tags">
                <span :key="family_manager.pk" v-for="family_manager in family.managers" class="group-id-tag group-id-manager-name" >
                    {{ family_manager.first_name }} {{ family_manager.last_name }}
                </span>
                <span v-if="family.inGroup" class="group-id-tag group-id-tag-fav">Member</span>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import VueProgressiveImage from 'vue-progressive-image'

Vue.use(VueProgressiveImage)

export default {
    props: {
        family: Object,
    },
    methods: {
        openModal(mofal_family){
            this.$emit('open-modal', mofal_family);
        }
    },
    computed: {
    }
}
</script>

<style scoped lang="css">
    *{
        box-sizing: border-box;
    }

    .card-body{
        font-family: Gill Sans, sans-serif;
    }

    .progressive-image:hover{
        opacity: 0.45;
        transition: .5s ease;
    }

    .progressive-image {
        transition: .5s ease;
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
        font-size: 15px;
        font-weight: 500;
        padding: 2px 6px 2px 6px;
        margin: 5px 4px 0px 0px;
        border-radius: 4px;
    }

    .group-id-tag-fav{
        color:#ffffff;
        background: rgba(245, 69, 172, 0.993);
    }

    .group-id-manager-name{
        color:#ffffff;
        background-color: rgb(23, 223, 196);
    }
</style>