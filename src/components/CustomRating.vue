<template>
    <v-card>
        <v-card-title>Rating</v-card-title>
        <v-card-text>
            <v-layout row>
                <v-flex class="rating-div" xs5 sm5 md6 lg6 xl6>
                    <div class="rating-span">{{rating == 0 ? 'N/A' : rating }}</div>
                    <v-rating
                        v-model="rating"
                        color="yellow darken-3"
                        background-color="grey darken-1"
                        readonly
                        medium
                        half-increments>
                    </v-rating>
                </v-flex>
                <v-flex xs7 sm7 md6 lg6 xl6>
                    <div class="five-ratings-div" :key="rating_index + '-rating' " v-for="rating_index in 5">
                        <v-rating
                            v-model="rating_default[rating_index - 1]"
                            readonly
                            half-increments>
                            <template v-slot:item="props">
                                <v-icon
                                small
                                :color=" (props.index < rating_index - 1 ) ? 'white' : 'grey lighten-1' ">
                                mdi-star
                                </v-icon>
                            </template>
                        </v-rating>
                        <v-flex>
                        <v-progress-linear
                            rounded
                            color="yellow darken-3"
                            :value="100 * counter[6 - rating_index]/counter_sum">
                            </v-progress-linear>
                        </v-flex>
                    </div>
                </v-flex>
            </v-layout>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions v-if="actiontext.length > 0">
            <v-spacer></v-spacer>
            <div class="rating-action">
            {{actiontext}}
            </div>
        </v-card-actions>
    </v-card>
</template>

<script>
    export default {
        props: {
            rating: Number,
            counter:Array,
            actiontext:String,
        },
        data() {
            return {
                rating_default:[5,4,3,2,1],
            }
        },
        components:{
        },
        computed:{
            counter_sum(){
                var sum = 0;
                for(let key in this.counter){
                    sum += this.counter[key];
                }
                return sum;
            },
        },
        methods: {
        },
    };
</script>

<style scoped lang="css">

    .rating-action{
        color:rgb(145, 145, 145);
        font-size:13px;
    }

    .v-progress-linear{
        justify-content: center;
        align-content: center;
    }

    .five-ratings-div{
        display:flex;
    }

    .five-ratings-div > .v-rating > .v-icon{
        padding: 1px;
    }

    .rating-div > .v-rating > .v-icon{
        padding: 5px;
    }

    .rating-num-span{
        font-size: 14px;
    }

    .rating-span{
        font-size: 38px;
        margin: 10px 0px 13px 0px;
        line-height: 40px;
        color: black;
    }

    .rating-div{
        text-align: center;
    }

    @media (min-width: 10px) and (max-width: 767px) {

        .rating-div > .v-rating > .v-icon{
            padding: 2.0px !important;
        }
    }

</style>