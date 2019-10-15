<template>
    <v-breadcrumbs class="cus-breadcrumbs" :items="items" divider="/">
        <template v-slot:item="props">
            <v-breadcrumbs-item
            :href="props.item.href"
            :disabled="props.item.disabled"
            >
                <v-btn 
                    :color="props.item.disabled ? 'grey' : 'teal darken-1' "
                    rounded
                    outlined>
                {{ props.item.text }}
                </v-btn>
            </v-breadcrumbs-item>
        </template>
    </v-breadcrumbs>
</template>

<script>
    export default {
        props: {
            items: Array,
        },
        data: () => ({

        }),
    }
</script>

<style>
    .v-breadcrumbs__item{
        padding-bottom: 10px;
    }

    .v-breadcrumbs__divider{
        padding-bottom: 10px !important;
    }

    .v-breadcrumbs{
        padding:9px 6px 2px 6px !important;
    }
    
</style>