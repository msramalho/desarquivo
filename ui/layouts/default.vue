<template>
  <v-app dark>
    <v-app-bar color="primary" dark app>
      <a class="main-link" to="/" @click="goHome">
        <logo />
      </a>
      <v-spacer />
      <examples />
      <instructions />
      <v-tooltip left>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            class="mx-2"
            href="https://github.com/msramalho/desarquivo"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon large>mdi-github</v-icon>
          </v-btn>
        </template>
        <span>{{ $t('default.source_code') }}</span>
      </v-tooltip>

      <v-tooltip left>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            class="mx-2"
            v-on:click="changeLang"
            v-bind="attrs"
            v-on="on"
          >{{lang == "pt" ? "en" : "pt"}}</v-btn>
        </template>
        <span>{{ $t('default.change_lang') }}</span>
      </v-tooltip>
    </v-app-bar>
    <v-content>
      <v-container class="pa-0 flex-grow-1" fluid fill-height>
        <nuxt />
      </v-container>
    </v-content>
  </v-app>
</template>

<style>
html {
  overflow-y: hidden !important;
}
/* scroll bar */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #e0f2f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #00897b;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #00695c;
}
.main-link span {
  color: white !important;
}
.main-link .animate:hover {
  cursor: pointer !important;
}
</style>
<script>
import Instructions from "~/components/Instructions.vue";
import Examples from "~/components/Examples.vue";
import Logo from "~/components/Logo.vue";
export default {
  components: { Instructions, Examples, Logo },
  data() {
    return {
      lang: this.$cookies.get("app-lang") || this.$store.state.locale || "pt"
    };
  },
  mounted() {
    this.$i18n.locale = this.lang;
  },
  methods: {
    goHome: () => {
      document.location.href = "/";
    },
    changeLang() {
      // toggle between portuguese and english
      this.lang = this.lang == "pt" ? "en" : "pt";
      this.$store.commit("SET_LANG", this.lang);
      this.$cookies.set("app-lang", this.lang);
      this.$i18n.locale = this.lang;
    }
  }
};
</script>
