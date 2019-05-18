<template>
    <div class="card user-card-min">
        <div class="user-card-min-inner">
            <img v-if="tmp_user.picture" class="card-img-top" :src="tmp_user.picture" alt="none">
            <div class="card-body">
                <div class="title d-flex w-100 justify-content-between">
                    <h5 class="mb-1 font-weight-bold">
                        {{tmp_user.first_name}} {{tmp_user.last_name}}
                    </h5>
                    <small style="float:right;">{{ tmp_user.year }}</small>
                </div>
                <div class="title d-flex w-100 justify-content-between">
                    <small v-if="tmp_user.major" class="text-muted">Major: {{ tmp_user.major }}</small>
                </div>
            </div>
        </div>
    </div>
</template>


<script>

export default {
    props: {
      tmp_user: Object,
    },
    mixins: [],
    computed: {
    }
}
</script>

<style scoped lang="css">
    .user-card-min{
        margin: 5px 3px 2px 3px;
    }   
</style>