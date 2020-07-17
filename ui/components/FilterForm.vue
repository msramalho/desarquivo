<template>
  <v-card
    max-width="500px"
    fixed
    raised
    :style="{position:'absolute', opacity:0.92}"
    class="ma-6"
    :loading="loadingCard"
  >
    <v-container>
      <h3 class="text-center pt-2" absolute>
        {{$t("filter_form.title")}}
        <!-- <v-btn icon @click="showFullForm = !showFullForm"  right>
          <v-icon>{{ showFullForm ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-btn>-->
      </h3>
      <v-row>
        <v-col>
          <v-autocomplete
            flat
            solo
            outlined
            dense
            prepend-inner-icon="mdi-magnify"
            :label="$t('filter_form.search_label')"
            v-model="select"
            :loading="loading"
            :items="items"
            :search-input.sync="search"
            :filter="()=>true"
            DONT-cache-items
            hide-details
            hide-no-data
            return-object
            auto-select-first
            loader-height="4"
            ref="searchBox"
          >
            <template v-slot:no-data>
              <v-list-item>
                <v-list-item-title>{{$t("filter_form.nothing_to_show")}}</v-list-item-title>
              </v-list-item>
            </template>

            <template v-slot:item="data">
              <template v-if="typeof data.item !== 'object'">
                <v-list-item-content v-text="data.item"></v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-content>
                  <v-list-item-title v-html="data.item.text"></v-list-item-title>
                  <v-list-item-subtitle class="text-small">
                    <v-icon small v-if="data.item.label=='PER'">mdi-account-outline</v-icon>
                    <v-icon small v-else-if="data.item.label=='ORG'">mdi-office-building</v-icon>
                    <v-icon small v-else-if="data.item.label=='LOC'">mdi-map-marker</v-icon>
                    <v-icon small v-else-if="data.item.label=='MISC'">mdi-dots-horizontal</v-icon>
                    {{data.item.label_pt}}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </template>
            </template>
          </v-autocomplete>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0 mt-3">
          <div
            class="text-center body-2"
          >{{$t("filter_form.expand.title")}} {{!(limit >= labels.length - 1)?` ${$t("basic.as")} ${labels[limit]} ${$t("filter_form.expand.most")}`:$t("filter_form.expand.all")}}</div>
          <v-slider
            v-model="limit"
            :tick-labels="labels"
            :max="labels.length - 1"
            step="1"
            ticks="always"
            tick-size="4"
          ></v-slider>
        </v-col>
      </v-row>
      <div
        class="text-center body-2 mt-3"
      >{{$t("filter_form.expand.and_search")}} {{searchLabels.length}} {{searchLabels.length==1?$t("filter_form.expand.singular"):$t("filter_form.expand.plural")}}</div>
      <v-row justify="space-around" class="mx-2 py-0">
        <v-checkbox
          v-model="searchLabels"
          color="#009688"
          :label="$t('filter_form.types.people')"
          value="PER"
          class="mt-1"
        ></v-checkbox>
        <v-checkbox
          v-model="searchLabels"
          color="#673AB7"
          :label="$t('filter_form.types.orgs')"
          value="ORG"
          class="mt-1"
        ></v-checkbox>
        <v-checkbox
          v-model="searchLabels"
          color="#00B8D4"
          :label="$t('filter_form.types.places')"
          value="LOC"
          class="mt-1"
        ></v-checkbox>
        <v-checkbox
          v-model="searchLabels"
          color="#263238"
          :label="$t('filter_form.types.others')"
          value="MISC"
          class="mt-1"
        ></v-checkbox>
      </v-row>
      <v-row>
        <v-col>
          <div
            class="text-center body-2"
          >{{$t("filter_form.connections")}} {{weightRange[0]}}% {{$t("basic.and")}} {{weightRange[1]}}%</div>
          <v-range-slider
            v-model="weightRange"
            hide-details
            class="align-center"
            min="0"
            max="100"
            step="1"
          ></v-range-slider>
        </v-col>
      </v-row>
      <div class="text-center body-2 mb-2">{{$t("filter_form.arrangement.title")}}</div>
      <v-row justify="space-around">
        <v-btn
          small
          color="primary"
          v-on:click="emit('runLayout', 'cose')"
        >{{$t("filter_form.arrangement.spaced")}}</v-btn>
        <v-btn
          small
          color="primary"
          v-on:click="emit('runLayout', 'fCose')"
        >{{$t("filter_form.arrangement.radial")}}</v-btn>
        <v-btn
          small
          color="primary"
          v-on:click="emit('runLayout', 'concentric')"
        >{{$t("filter_form.arrangement.concentric")}}</v-btn>
        <v-btn
          small
          color="primary"
          v-on:click="emit('runLayout', 'bfs')"
        >{{$t("filter_form.arrangement.breadth")}}</v-btn>
      </v-row>
      <div class="text-center body-2 mt-5">{{$t("filter_form.other_actions.title")}}</div>
      <v-row>
        <v-col class="py-0">
          <div class="text-center">
            <!-- <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  class="ma-2"
                  text
                  icon
                  color="primary"
                  v-on:click="emit('downloadJson')"
                  v-on="on"
                >
                  <v-icon>mdi-download</v-icon>
                </v-btn>
              </template>
              <span>Transferir JSON</span>
            </v-tooltip>-->

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  class="ma-2"
                  text
                  icon
                  color="primary"
                  v-on:click="emit('downloadPng')"
                  v-on="on"
                >
                  <v-icon>mdi-download</v-icon>
                </v-btn>
              </template>
              <span>{{$t("filter_form.other_actions.capture")}}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  class="ma-2"
                  text
                  icon
                  color="primary"
                  v-on:click="emit('invertSelection')"
                  v-on="on"
                >
                  <v-icon>mdi-select-inverse</v-icon>
                </v-btn>
              </template>
              <span>{{$t("filter_form.other_actions.invert")}}</span>
            </v-tooltip>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  class="ma-2"
                  text
                  icon
                  color="blue lighten-2"
                  v-on:click="emit('expandSelected')"
                  v-on="on"
                  :disabled="countSelectedNodes!=1"
                >
                  <v-icon>mdi-arrow-expand-all</v-icon>
                </v-btn>
              </template>
              <span>{{$t("filter_form.other_actions.expand_node")}}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  v-on:click="emit('intersectSelected')"
                  text
                  icon
                  v-on="on"
                  color="cyan"
                  :disabled="countSelectedNodes<2"
                >
                  <v-icon>mdi-set-center</v-icon>
                </v-btn>
              </template>
              <span>{{$t("filter_form.other_actions.keep_selected")}}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  v-on:click="emit('connectSelectedSingle')"
                  text
                  icon
                  v-on="on"
                  color="orange"
                  :disabled="countSelectedNodes!=2"
                >
                  <v-icon>mdi-handshake</v-icon>
                </v-btn>
              </template>
              <span>{{$t("filter_form.other_actions.direct_link")}}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  v-on:click="emit('connectSelected')"
                  text
                  icon
                  v-on="on"
                  color="orange darken-2"
                  :disabled="countSelectedNodes!=2"
                >
                  <!-- <v-icon>mdi-google-circles-extended</v-icon> -->
                  <v-icon>mdi-transit-connection</v-icon>
                </v-btn>
              </template>
              <span>{{$t("filter_form.other_actions.common_links")}}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  color="error"
                  v-on:click="emit('deleteSelected')"
                  text
                  icon
                  v-on="on"
                  :disabled="countSelectedNodes==0"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
              <span>{{$t("filter_form.other_actions.delete.pre")}} {{countSelectedNodes}} {{countSelectedNodes==1?$t("filter_form.other_actions.delete.singular"):$t("filter_form.other_actions.delete.plural")}}</span>
            </v-tooltip>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <!-- <v-expand-transition>
      <div v-show="showFullForm">
        <v-divider></v-divider>
        <v-card-text>I'm a thing. But, like most politicians, he promised more than he could deliver. You won't have time for sleeping, soldier, not with all the bed making you'll be doing. Then we'll go with that data file! Hey, you add a one and two zeros to that or we walk! You're going to do his laundry? I've got to find a way to escape.</v-card-text>
      </div>
    </v-expand-transition>-->
  </v-card>
</template>

<style scoped>
.text-small {
  font-size: 0.8em;
}
</style>

<script>
export default {
  props: {
    countSelectedNodes: Number,
    countSelectedEdges: Number,
    loadingCard: Boolean
  },
  data() {
    return {
      loading: false,
      items: [],
      search: null,
      select: null,
      limit: 1,
      labels: [30, 50, 150, 300, "100%"], // ∞
      searchLabels: ["PER", "ORG", "LOC", "MISC"],
      weightLabels: ["0", "", "", "", "", "", "", "", "", "", "100%"],
      weightRange: [0, 100],
      showFullForm: true
    };
  },
  watch: {
    search(val) {
      val &&
        val !== this.select &&
        val.length >= 2 &&
        this.querySelections(val);
    },
    select(chosen) {
      if (chosen == null) return;
      this.$emit("selectEntity", chosen);
      this.select = null;
    },
    limit(_new) {
      this.$emit("updateLimit", _new);
    },
    searchLabels(_new) {
      this.$emit("updateSelectedLabels", _new);
    },
    weightRange(range) {
      this.$emit("updateFilterRange", { min: range[0], max: range[1] });
    }
  },
  methods: {
    querySelections(v) {
      // a request is in process
      setTimeout(() => {
        if (v != this.search) return;
        if (this.select && this.select.text == this.search) return;
        if (this.loading) return;

        this.loading = true;
        // Simulated ajax query
        this.$axios
          .get("/search", {
            params: {
              query: this.search
            }
          })
          .then(res => {
            this.items = res.data.results;
          })
          .catch(e => {
            this.$toast.error(this.$t("filter_form.errors.communication"), {
              x: "right",
              y: "bottom",
              timeout: 4000
            });
          })
          .finally(() => (this.loading = false));
      }, 300);
    },
    emit(functionName, param) {
      this.$emit(functionName, param);
    },
    keydown(e) {
      if (e.key == "f" && e.ctrlKey) {
        e.preventDefault();
        this.$refs.searchBox.focus();
      }
    }
  },
  created: function() {
    window.addEventListener("keydown", this.keydown);
  },
  beforeDestroy: function() {
    window.removeEventListener("keydown", this.keydown);
  }
};
</script>
