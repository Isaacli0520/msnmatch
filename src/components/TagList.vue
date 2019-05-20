<template>
    <div>
        <div v-for="(skills_of_type, skills_type_name) in all_skills">
            <h4 class="skill-type-text">{{skill_type_names[skills_type_name]}}</h4>
            <div class="skill-tags">
                <tag-span v-for="skill in skills_of_type"
                    v-bind:key="skill.skill_pk"
                    v-bind:skill="skill"
                    v-bind:clickable="'add'"
                    @add-skill="add_skill"
                    @del-skill="del_skill"
                />
            </div>
        </div>
    </div>
</template>

<script>
import TagSpan from "./TagSpan"

export default{
    props:{
        "all_skills":Object,
    },
    components:{
        TagSpan,
    },
    data: function () {
            return {
                skill_type_names: {
                    "Game":"Game",
                    "Academic":"Academic Interests",
                    "Film and TV":"Film and TV",
                    "Sport":"Sport",
                    "Music":"Music",
                    "Language":"Language",
                    "General":"General",
                    "Books":"Books",
                },
            }
        },
    methods:{
        add_skill(skill){
            this.$emit('add-skill', skill);
            this.all_skills[skill.skill_type].splice(this.all_skills[skill.skill_type].indexOf(skill), 1);
        },
        del_skill(skill){
            this.$emit('del-skill', skill);
        },
    },
    mounted(){
    },
    }
</script>

<style scoped lang="css">
    .skill-type-text{
        color: #32a49a;
        font-family: Palatino, URW Palladio L, serif;
    }

    .skill-tags{
        display: flex;
        flex-flow: row wrap;
        width:100%;
        margin: 5px 0px 20px 0px;
    }
</style>