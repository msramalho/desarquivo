<template>
  <v-dialog max-width="900" eager>
    <template v-slot:activator="{ on }">
      <v-btn large outlined v-on="on" class="mr-2">
        {{$t("instructions.title")}}
        <!-- <v-icon class="pl-2">mdi-information-outline</v-icon> -->
        <!-- <v-icon class="pl-2">mdi-help</v-icon> -->
      </v-btn>
    </template>

    <v-card style="overflow-x: hidden;">
      <v-card-title
        class="headline primary text-center"
        primary-title
        style="color:white; display:block;"
      >
        <logo />
        <br />
        <span class="font-italic body-1" v-html="$t('instructions.motto')"></span>
      </v-card-title>

      <v-card-text class="ma-4 pa-2" style="width:96%">
        <p
          class="body-1 mb-2 text-center font-weight-medium"
          v-html="$t('instructions.short_description')"
        ></p>
        <p class="body-1 text-center" v-html="$t('instructions.description')"></p>
      </v-card-text>
      <v-expansion-panels accordion hover popout class="mb-5">
        <v-expansion-panel>
          <v-expansion-panel-header>
            {{$t('instructions.expansion_instructions.title')}}
            <span
              class="lide text--secondary mr-10 text-right"
            >{{$t('instructions.expansion_instructions.question')}}</span>
            <template v-slot:actions>
              <v-icon color="primary">$expand</v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content class="ma-2 mt-5 body-2">
            <!-- instructions -->
            <p class="m-title text-center mb-2">
              <v-icon>mdi-magnify</v-icon>
              &nbsp;{{$t("instructions.expansion_instructions.search.title")}}
            </p>
            <span v-html="$t('instructions.expansion_instructions.search.content')"></span>
            <!-- expand -->
            <p class="m-title text-center mb-2 mt-7">
              <v-icon>mdi-arrow-expand-all</v-icon>
              &nbsp;{{$t("instructions.expansion_instructions.expand.title")}}
            </p>
            <span v-html="$t('instructions.expansion_instructions.expand.content')"></span>
            <!-- filtrar -->
            <p class="m-title text-center mb-2 mt-7">
              <v-icon>mdi-filter</v-icon>
              &nbsp;{{$t("instructions.expansion_instructions.filter.title")}}
            </p>
            <span v-html="$t('instructions.expansion_instructions.filter.content')"></span>
            <!-- investigate -->
            <p class="m-title text-center mb-2 mt-7">
              <v-icon>mdi-account-search-outline</v-icon>
              &nbsp;{{$t("instructions.expansion_instructions.investigate.title")}}
            </p>
            <span v-html="$t('instructions.expansion_instructions.investigate.content')"></span>
            <ul>
              <li>
                <kbd>
                  <v-icon small color="white">mdi-set-center</v-icon>
                </kbd>
                <span v-html="$t('instructions.expansion_instructions.investigate.item0')"></span>
              </li>
              <li>
                <kbd>
                  <v-icon small color="white">mdi-handshake</v-icon>
                </kbd>
                <span v-html="$t('instructions.expansion_instructions.investigate.item1')"></span>
              </li>
              <li>
                <kbd>
                  <v-icon small color="white">mdi-transit-connection</v-icon>
                </kbd>
                <span v-html="$t('instructions.expansion_instructions.investigate.item2')"></span>
              </li>
            </ul>
            <!-- visualize -->
            <p class="m-title text-center mb-2 mt-7">
              <v-icon>mdi-graphql</v-icon>
              &nbsp;{{$t("instructions.expansion_instructions.visualize.title")}}
            </p>
            <span v-html="$t('instructions.expansion_instructions.visualize.content')"></span>
            <!-- news -->
            <p class="m-title text-center mb-2 mt-7">
              <v-icon>mdi-newspaper</v-icon>
              &nbsp;{{$t("instructions.expansion_instructions.news.title")}}
            </p>
            <span v-html="$t('instructions.expansion_instructions.news.content')"></span>
            <!-- shortcuts -->
            <p class="m-title text-center mb-2 mt-7">
              <v-icon>mdi-keyboard</v-icon>
              &nbsp;{{$t("instructions.expansion_instructions.shortcuts.title")}}
            </p>
            <span v-html="$t('instructions.expansion_instructions.shortcuts.content')"></span>
            <!-- final notes -->
            <p
              class="m-title text-center mt-7"
            >{{$t("instructions.expansion_instructions.notes.title")}}</p>
            <span v-html="$t('instructions.expansion_instructions.notes.content')"></span>
            <kbd>
              <v-icon small color="white">mdi-download</v-icon>
            </kbd>.
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>
            {{$t("instructions.expansion_about.title")}}
            <span
              class="lide text--secondary mr-10 text-right"
            >{{$t("instructions.expansion_about.question")}}</span>
            <template v-slot:actions>
              <v-icon color="primary">$expand</v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content class="ma-2 mt-5 body-2">
            <v-row align="center" class="justify-center mt-5 mb-7">
              <iframe
                width="560"
                height="315"
                src="https://www.youtube.com/embed/tVlOUuRqIVU"
                frameborder="0"
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                class="elevation-5"
                allowfullscreen
              ></iframe>
            </v-row>
            <span v-html="$t('instructions.expansion_about.content')"></span>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>
            {{$t("instructions.expansion_context.title")}}
            <span
              class="lide text--secondary mr-10 text-right"
            >{{$t("instructions.expansion_context.question")}}</span>
            <template v-slot:actions>
              <v-icon color="primary">$expand</v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content class="ma-2 mt-5 body-2">
            <p v-html="$t('instructions.expansion_context.content')"></p>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>
            {{$t("instructions.expansion_author.title")}}
            <span
              class="lide text--secondary mr-10 text-right"
            >{{$t("instructions.expansion_author.question")}}</span>
            <template v-slot:actions>
              <v-icon color="primary">$expand</v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content class="ma-2 mt-5 body-2">
            <v-row>
              <v-col :cols="3" class="text-center justify-center">
                <v-img
                  :src="require('~/assets/autor.jpg')"
                  max-height="100"
                  max-width="100"
                  eager
                  class="mx-auto"
                  style="border-radius:50px;"
                  alt="foto de perfil de Miguel Ramalho"
                ></v-img>
                <span>Miguel Ramalho</span>
              </v-col>
              <v-col :cols="9" align-self="center">
                <!-- v-html="$t('instructions.expansion_author.content') -->
                {{$t("instructions.expansion_author.content.pre")}}
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <a
                      v-on="on"
                      href="https://sigarra.up.pt/feup/pt/cur_geral.cur_view?pv_curso_id=742"
                    >MIEIC</a>
                  </template>
                  <span>{{$t("instructions.expansion_author.content.mieic")}}</span>
                </v-tooltip>
                &nbsp;{{$t("instructions.expansion_author.content.dur")}}
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <a v-on="on" href="https://sigarra.up.pt/feup/pt/web_page.Inicial">FEUP</a>
                  </template>
                  <span>{{$t("instructions.expansion_author.content.feup")}}</span>
                </v-tooltip>.
                <br />
                <span v-html="$t('instructions.expansion_author.content.rest')"></span>
              </v-col>
            </v-row>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>
            {{$t("instructions.expansion_open_source.title")}}
            <template v-slot:actions>
              <v-icon color="primary">$expand</v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content class="ma-2 mt-5 body-2">
            <span v-html="$t('instructions.expansion_open_source.content')"></span>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.m-title {
  font-size: 1.15em;
}
ul > li > ul > li {
  font-size: 0.8em;
}
.v-expansion-panel-header.v-expansion-panel-header--active {
  background-color: #00bfa5;
  color: white;
  font-size: 1.2em;
}
.v-expansion-panel-header.v-expansion-panel-header--active .lide {
  display: none;
}
.v-expansion-panel-header.v-expansion-panel-header--active .v-icon {
  color: white !important;
}
</style>

<script>
import Logo from "~/components/Logo.vue";
export default {
  components: { Logo }
};
</script>
