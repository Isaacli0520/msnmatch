<template>
    <a
        :class="['skill-tag',skill.type, (clickable =='delete') ? 'skill-tag-del' : 'skill-tag-add']"
        v-on="clickable!='delete' ? { click: () => add_skill(skill) } : {}">
        <span>{{skill.name}}</span>
        <span v-if="clickable=='delete' " class="skill-tag-remove">
            <v-icon 
                style="margin-bottom:2px;"
                small 
                color="white" 
                @click="del_skill(skill)"
                >
                mdi-close-thick
            </v-icon>
        </span>
    </a>
</template>

<script>

export default{
    props:{
        skill:Object,
        clickable: String,
    },
    methods:{
        add_skill(skill){
            if(this.clickable == "add")
                this.$emit('add-skill', skill);
            // else if(this.clickable == "href")
            //     window.location.href = "/skills/"+ skill.id.toString(10);
        },
        del_skill(skill){
            this.$emit('del-skill', skill);
        }

    },
}

</script>


<style scoped lang="css">
    *{
        box-sizing: border-box;
    }
    .skill-tag{
        padding: 5px 9px 5px 9px;
        border-radius: 5px;
        margin: 5px 7px 5px 0px;
        opacity: 1;
        transition: .5s ease;
        font-family: Gill Sans, sans-serif;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.175);
    }

    .skill-tag-del{
        padding: 5px 5px 5px 9px;
    }

    .skill-tag-add{
        padding: 5px 9px 5px 9px;
    }

    a.skill-tag-add:hover{
        opacity: 0.7;
        /* color:#000000; */
    }

    span.skill-tag-remove{
        transition: .5s ease;
    }

    span.skill-tag-remove:hover{
        color: #494949;
    }

    .skill-tag span{
        color: #ffffff;
    }

    .skill-tag-remove{
        margin:0px 1px 0px 3px;
    }

    .MBTI{
        color:#ffffff;
        background-color: #ff6b6b;
    }

    .Academic{
        color:#ffffff;
        background-color:#f06595;
    }

    .Books{
        color:#ffffff;
        background-color:#cc5de8;
    }

    .Film{
        color:#ffffff;
        background-color:#9775fa;
    }
        
    .Game{
        color:#ffffff;
        background-color: #748ffc;
    }

    .Language{
        color:#ffffff;
        background-color:#74c0fc;
    }

    .Music{
        color:#ffffff;
        background-color: #20c997;
    }

    .Sport{
        color:#ffffff;
        background-color: #51cf66;
    }

    .General{
        color:#ffffff;
        background-color: #fab005;
    }

    .Custom{
        color:#ffffff;
        background-color: #ff922b;
    }
</style>