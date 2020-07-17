<template>
  <div>
    <v-card
      style="background: #fff; position:absolute; top:0; right:0; z-index:25; width: 370px"
      class="px-4 ma-4"
      :loading="loading || loadingIds"
    >
      <v-list-item dense>
        <h3 :class="{'text--disabled':!loadNews}" class="mx-auto">
          <v-icon :disabled="!loadNews" left color="primary">mdi-newspaper</v-icon>
          {{$t('news.title')}}
          <small v-if="show && loadNews">{{newsText}}</small>
        </h3>
        <v-tooltip bottomn>
          <template v-slot:activator="{ on }">
            <v-switch
              v-on="on"
              v-model="loadNews"
              hide-details
              class="ma-0 pa-0"
              style="position: absolute; right: 0"
            ></v-switch>
          </template>
          <span>{{loadNews?$t('news.activate'):$t('news.deactivate')}} {{$t('news.toggle_message')}}</span>
        </v-tooltip>
      </v-list-item>
      <small
        class="d-block text-center"
        :class="{'mb-2': !newsParts || newsParts.length<=1}"
        v-if="show && loadNews"
        v-html="displayTextComp"
      ></small>
      <v-row class="ma-0 pa-0">
        <v-slider
          class="ma-0"
          v-if="newsParts && newsParts.length>1"
          dense
          hide-details
          v-model="date"
          :min="0"
          :max="newsParts.length - 1"
          v-on:end="updateNewsPart"
          v-on:mouseup="updateNewsPart"
          ticks="always"
          tick-size="4"
        ></v-slider>
      </v-row>
    </v-card>
    <v-navigation-drawer
      v-if="show && loadNews"
      right
      permanent
      absolute
      color="transparent"
      style="width: 400px"
    >
      <!-- https://vuetifyjs.com/en/components/slide-groups/ -->
      <!-- <v-timeline dense class="caption" style="position:absolute;top:60px;right:380px;z-index:400">
        <v-timeline-item small right>2020</v-timeline-item>
        <v-timeline-item small right>2019</v-timeline-item>
        <v-timeline-item small right>2015</v-timeline-item>
      </v-timeline>-->
      <v-list class="pt-0">
        <v-divider></v-divider>
        <div
          v-if="loadNews"
          style="z-index: 20;"
          :style="{'margin-top': newsParts && newsParts.length>1?`105px`:`80px`}"
        >
          <v-list-item class="pt-3" v-for="n in news" :key="n._id">
            <v-card class="mx-auto" color="#eaeff2" shaped>
              <v-list-item three-line>
                <v-list-item-content class="pb-0" two-line>
                  <v-tooltip left>
                    <template v-slot:activator="{ on }">
                      <v-list-item-title v-on="on" class="subtitle-2 mb-0">{{n.title}}</v-list-item-title>
                    </template>
                    <span>{{n.title}}</span>
                  </v-tooltip>
                  <v-list-item-subtitle :title="n.text" class="multiline">{{n.text}}</v-list-item-subtitle>
                  <small
                    class="caption font-weight-medium text-left mt-1"
                  >{{timestampToText(n.timestamp)}}</small>
                </v-list-item-content>

                <v-list-item-avatar v-if="n.image" lazy-src tile size="60">
                  <v-img :src="n.image" v-on:error="n.image=null"></v-img>
                </v-list-item-avatar>
              </v-list-item>

              <!-- <v-divider class="my-2"></v-divider> -->

              <v-card-actions class="d-flex flex-row">
                <v-row>
                  <v-col>
                    <v-btn small text outlined @click="n.expanded = !n.expanded">
                      <v-icon>{{ n.expanded ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                      {{$t('news.entities')}}
                    </v-btn>
                  </v-col>
                  <v-col>
                    <v-btn
                      small
                      text
                      outlined
                      :href="n.url"
                      target="_blank"
                      color="blue-grey"
                      class="white--text"
                    >
                      {{$t('news.original')}}
                      <v-icon right dark>mdi-open-in-new</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-actions>

              <v-expand-transition>
                <div v-show="n.expanded" class="ma-2 text-center">
                  <entity-chip :entities="n.entities.PER" label="PER" v-on:addEntity="addEntity" />
                  <entity-chip :entities="n.entities.ORG" label="ORG" v-on:addEntity="addEntity" />
                  <entity-chip :entities="n.entities.LOC" label="LOC" v-on:addEntity="addEntity" />
                  <entity-chip :entities="n.entities.MISC" label="MISC" v-on:addEntity="addEntity" />
                </div>
              </v-expand-transition>
            </v-card>
          </v-list-item>
        </div>

        <v-list-item
          v-if="loading || waiting"
          class="pt-3 justify-center"
          v-intersect="infiniteScroll"
        >
          <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<style scoped>
.multiline {
  -webkit-line-clamp: 5;
  max-height: 65px;
}
</style>

<script>
import EntityChip from "~/components/EntityChip.vue";
import { setup } from "axios-cache-adapter";
import memoryDriver from "localforage-memoryStorageDriver";
import localforage from "localforage";

async function configure(baseURL) {
  await localforage.defineDriver(memoryDriver);
  const forageStore = localforage.createInstance({
    driver: [
      localforage.INDEXEDDB,
      localforage.LOCALSTORAGE,
      memoryDriver._driver
    ],
    name: "desarquivo-cache"
  });
  return setup({
    baseURL: baseURL,
    cache: {
      maxAge: 15 * 60 * 1000, // 15min cache
      store: forageStore // Pass `localforage` store to `axios-cache-adapter`
    }
  });
}

export default {
  props: {
    selectedEdge: Object,
    selectedNode: Object,
    show: Boolean,
    displayText: String
  },
  data() {
    return {
      loadNews: true,
      loading: false,
      loadingIds: false,
      waiting: false,
      page: 0,
      news: [],
      newsIds: [],
      newsParts: undefined,
      newsFromIndex: 0,
      date: 0,
      dateStr: undefined,
      dateRange: [0, 0]
    };
  },
  mounted: function() {
    this.api = this.$axios;
    configure(this.$axios.defaults.baseURL).then(api => {
      // this.api = this.$axios.create({ adapter: cache.adapter });
      this.api = api;
    });
  },
  computed: {
    newsText: function() {
      if (this.newsIds.length == 0) return "";
      return `${this.newsFromIndex + this.news.length}/${this.newsIds.length}`;
    },
    displayTextComp() {
      if (!this.dateStr) return this.displayText;
      return `${this.displayText} - ${this.$t("news.before")} ${this.dateStr}`;
    }
  },
  watch: {
    newsIds(val) {
      if (val.length == 0) return;
      this.displayNews();
    },
    selectedEdge(edge) {
      if (!this.loadNews || !edge) return;

      this.actionSelectEdge(edge);
    },
    selectedNode(node) {
      if (!this.loadNews || !node) return;
      this.actionSelectNode(node);
    },
    page(p) {
      this.waiting =
        this.newsFromIndex + this.news.length < this.newsIds.length;
    },
    loadNews(val) {
      if (!val) return;
      this.forceLoadNews();
    }
  },
  methods: {
    forceLoadNews() {
      if (this.selectedEdge != null) this.actionSelectEdge(this.selectedEdge);
      else if (this.selectedNode != null)
        this.actionSelectNode(this.selectedNode);
    },
    actionSelectEdge(edge) {
      this.getNewsIds("/edge_news", { from: edge.source, to: edge.target });
    },
    actionSelectNode(node) {
      this.getNewsIds("/entity_news", { _id: node.id });
    },
    updateNewsPart() {
      setTimeout(() => {
        this.dateStr = this.timestampToText(this.newsParts[this.date][1]);
        this.newsFromIndex = this.newsParts[this.date][2];
        this.page = 0;
        this.news = [];
        this.displayNews();
      }, 100);
    },
    getNewsIds(endpoint, params) {
      if (this.loadingIds) return;
      this.loadingIds = true;
      this.newsIds = [];
      this.news = [];
      this.api
        .get(endpoint, { params })
        .then(res => {
          this.page = 0;
          this.newsFromIndex = 0;
          this.newsIds = res.data.news_ids;
          this.newsParts = res.data.parts;
          if (this.newsParts.length > 1) {
            this.date = 0;
            this.dateStr = this.timestampToText(this.newsParts[0][1]);
          }
        })
        .catch(e => {
          this.$toast.error(this.$t("news.errors.communication"), {
            x: "right",
            y: "bottom",
            timeout: 4000
          });
        })
        .finally(() => (this.loadingIds = false));
    },
    displayNews() {
      if (this.loading) return;
      if (!this.newsIds || !this.newsIds.length) return;

      this.loading = true;
      // console.log(
      //   this.newsFromIndex + 20 * this.page,
      //   this.newsFromIndex + 20 * (this.page + 1)
      // );
      this.api
        .get("/news", {
          params: {
            news_ids: this.newsIds
              .slice(
                this.newsFromIndex + 20 * this.page,
                this.newsFromIndex + 20 * (this.page + 1)
              )
              .join()
          }
        })
        .then(res => {
          this.news.push(
            ...res.data.news.map(n => {
              n.expanded = false;
              return n;
            })
          );
          this.page += 1;
        })
        .catch(e => {
          this.$toast.error(this.$t("news.errors.communication_ask"), {
            x: "right",
            y: "bottom",
            timeout: 4000
          });
        })
        .finally(() => (this.loading = false));
    },
    addEntity(e) {
      this.$emit("addEntity", e);
    },
    timestampToText(timestamp) {
      let t = new Date(Date.parse(timestamp));
      return `${t.getDate()} ${this.month(t.getMonth())} ${t.getFullYear()}`;
    },
    infiniteScroll(entries, observer, isIntersecting) {
      if (isIntersecting && this.waiting) this.displayNews();
    },
    keyup(e) {
      if (document.activeElement.nodeName == "INPUT") return;
      if (e.key == "n") this.loadNews = !this.loadNews;
    },
    month(m) {
      return this.$t("news.months")[m];
    }
  },
  created: function() {
    window.addEventListener("keydown", this.keyup);
  },
  beforeDestroy: function() {
    window.removeEventListener("keydown", this.keyup);
  },
  components: { EntityChip }
};
</script>