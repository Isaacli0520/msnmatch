<template>
    <div class="container">
        <div class="col-12 mb-5" style = "width:100%; margin: 0 auto;">
            <div class="container mt-5 mb-4 text-center">
                <h1 class="display-4 skill-main-title" >Add Your Interests</h1>
                <h6 class="text-muted">Search for existing tags or Add your own tags</h6>
            </div>
        </div>
        <div class="col-xs-12 col-sm-12 col-md-10 col-lg-8 col-xs-offset-0 col-sm-offset-0" id = "skill-list-app" style="width:100%; margin: 0 auto;">
            <div class="autocomplete mb-4" style="width:100%;">
                <autoComplete/>
            </div>
        </div>
    </div>
</template>

<script>
import AutoComplete from '../components/AutoComplete'

export default{
    data:function(){
        return {
            
        }
    },
    components:{
        AutoComplete,
    },
}

</script>

<style scoped lang="css">
    .skill-main-title{
        color:#32a49a; 
        font-family: Palatino, URW Palladio L, serif;
    }
</style>