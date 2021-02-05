<template>
    <v-card
        class="fill-height"
        outlined
        :ripple="false"
        elevation="3"
        :href="editable ? undefined : '/courses/' + review.course.pk + '/' + review.instructor.pk ">
        <v-card-title>
            <span class="review-headline-number">{{review.course.mnemonic}}{{review.course.number}}</span>
            <span class="review-headline-text">{{review.course.title}}</span></v-card-title>
        <v-card-subtitle class="review-instructor-name">{{review.instructor.name}}</v-card-subtitle>
        <v-card-text style="color:#000;padding-left: 18px !important;">
            <div class="review-text">{{ review.text }}</div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions style="flex-flow:row wrap !important;">
            <v-spacer v-if="$vuetify.breakpoint.lgAndUp"></v-spacer>
            <v-chip
                class="ma-1" :color="variables.secondary_color" label outlined small :text-color="variables.secondary_color">
                {{review.semester}}
            </v-chip>
            <v-chip
                class="ma-1" style="padding: 0px 5px 0px 9px !important;" :color="variables.primary_color"
                label outlined small>
                <span class="caption mr-1">Instructor:</span>
                <v-rating
                    style="margin-bottom:2px !important;"
                    v-model="review.rating_instructor"
                    color="yellow darken-2"
                    :background-color="variables.primary_color"
                    readonly
                    dense
                    small
                    half-increments>
                </v-rating>
            </v-chip>
            <v-chip
                class="ma-1" style="padding: 0px 5px 0px 9px !important;" :color="variables.primary_color"
                label outlined small>
                <span class="caption mr-1">Course:</span>
                <v-rating
                    style="margin-bottom:2px !important;"
                    v-model="review.rating_course"
                    color="yellow darken-2"
                    :background-color="variables.primary_color"
                    readonly
                    dense
                    small
                    half-increments>
                </v-rating>
            </v-chip>
            <v-chip
                v-if="editable"
                class="ma-1"
                outlined
                color="red"
                @click="editReview(review)"
                label 
                small>
                Edit
            </v-chip>
        </v-card-actions>
    </v-card>
</template>

<script>
import variables from '../sass/variables.scss'

export default{
    props:{
        review:Object,
        editable: Boolean,
    },
    data(){
        return {
            variables:variables,
        }
    },
    methods:{
        editReview(review){
            this.$emit('edit-review', review);
        }

    },
}

</script>


<style scoped lang="scss">

    .review-text{
        font-size: 16px;
        color:rgb(0, 0, 0);
        font-family: "Roboto", sans-serif;
        word-wrap:break-word;
        white-space: pre-line;
    }

    .review-instructor-name{
        color:#000;
        padding: 6px 16px 8px 18px !important;
        font-size:1.1em !important;
        border: black;
    }

    .review-headline-number{
        font-family: "Roboto", sans-serif;
        font-size: 1.1em;
        font-weight: 500;
        background-color: $primary-color;
        color:#fff;
        padding: 1px 7px 1px 7px;
        border-radius: 5px 0px 0px 5px;
        line-height: 1.4;
        box-decoration-break: clone;
    }

    .review-headline-text{
        font-family: "Roboto", sans-serif;
        font-size: 1.1em;
        font-weight: 300;
        background-color: $course-title-bg-color;
        color:$course-title-color;
        padding: 1px 7px 1px 7px;
        border-radius: 0px 5px 5px 0px;
        line-height: 1.4;
        box-decoration-break: clone;

    }

    @media (min-width: 10px) and (max-width: 767px) {
        .review-headline-instructor{
            font-size: 15px;
        }

        .review-headline-text{
            font-size: 15px;
        }

        .review-headline-number{
            font-size: 15px;;
        }
    }
</style>