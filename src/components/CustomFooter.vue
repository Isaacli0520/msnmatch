<template>
    <v-footer
        app
        padless
        absolute
        class="custom-footer">
        <v-card
        flat
        tile
        style="width:100%;"
        class="teal lighten-2 white--text text-center">
        <v-card-text>
            <v-btn
            v-for="item in icons"
            :key="item.icon"
            :target="item.target"
            :href="item.href"
            class="mx-4 white--text"
            icon
            >
            <v-icon size="24px">{{ item.icon }}</v-icon>
            </v-btn>
      </v-card-text>
        <v-card-text class="white--text pt-0 pl-10 pr-10">
            <p>Although this organization has members who are University of Virginia students and may have University employees associated or engaged in its activities and affairs, the organization is not a part of or an agency of the University. It is a separate and independent organization which is responsible for and manages its own activities and affairs. The University does not direct, supervise or control the organization and is not responsible for the organization’s contracts, acts or omissions.</p>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-text class="white--text">
            {{ new Date().getFullYear() }} — <strong>Mainland Student Network</strong>
        </v-card-text>
        </v-card>
    </v-footer>
</template>

<script>
  export default {
    data: () => ({
      icons: [
          {
              icon:"fab fa-facebook",
              href:"https://www.facebook.com/msnatuva",
              target:"_blank",
          },
          {
              icon:"fab fa-instagram",
              href:"https://www.instagram.com/msnatuva",
              target:"_blank",
          },
      ],
    }),
  }
</script>

<style scoped lang="css">
    .custom-footer{
        /* padding:50px 0px 0px 0px !important; */
        background-color:#fff !important;
        color:#fff !important;
    }
</style>