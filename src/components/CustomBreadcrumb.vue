<template>
    <v-breadcrumbs class="cus-breadcrumbs" large :items="items" divider="/">
        <template v-slot:item="props">
            <v-breadcrumbs-item
                style="padding:0px 0px 14px;"
                :href="props.item.href"
                :disabled="props.item.disabled"
                >
                <v-btn 
                    :color="props.item.disabled ? 'grey' : variables.primary_color "
                    rounded
                    outlined>
                {{ props.item.text }}
                </v-btn>
            </v-breadcrumbs-item>
        </template>
    </v-breadcrumbs>
</template>

<script>
import variables from '../sass/variables.scss'

export default {
    props: {
        items: Array,
    },
    data: () => ({
        variables: variables,
    }),
}
</script>

<style scoped lang="css">
    .v-breadcrumbs__item{
        padding-bottom: 10px;
    }

    .v-breadcrumbs__divider{
        padding-bottom: 10px !important;
    }

    .v-breadcrumbs{
        padding:9px 6px 0px 6px !important;
    }
    
</style>