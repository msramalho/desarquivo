<template>
  <v-dialog max-width="900" eager>
    <template v-slot:activator="{ on }">
      <v-btn large outlined v-on="on" class="mr-2">
        {{$t("examples.title")}}
        <v-icon class="pl-2">mdi-lightbulb-on-outline</v-icon>
      </v-btn>
    </template>

    <v-card style="overflow-x: hidden;">
      <v-card-title
        class="headline primary text-center"
        primary-title
        style="color:white; display:block;"
      >{{$t("examples.header")}}</v-card-title>

      <v-card-text class="pa-2">
        <v-slide-group v-model="model" class="pa-2" show-arrows>
          <v-slide-item v-for="item in items" :key="item.id" v-slot:default="{ active, toggle }">
            <v-card
              :color="active ? 'primary' : 'grey lighten-4'"
              class="ma-4 pa-2 text-center d-flex flex-column"
              height="200"
              width="200"
              @click="toggle"
              raised
            >
              <span
                class="mb-2 flex-grow-1 subtitle-1"
                :style="{color: active ? 'white' : 'inherit'}"
                v-html="$t(`examples.items.${item.id}.title`)"
              ></span>
              <v-img max-height="120px" aspect-ratio="1" :src="item.src" style="border-radius:5px;"></v-img>
            </v-card>
          </v-slide-item>
        </v-slide-group>

        <v-expand-transition>
          <v-sheet
            v-if="model != null"
            color="transparent"
            class="px-8 text-center"
            min-height="200"
          >
            <v-row class="pt-5 mx-5">
              <v-col>
                <v-row class="mb-4" justify="center">
                  <h3 class="subtitle-1">{{ $t(`examples.items.${items[model].id}.description`) }}</h3>
                </v-row>
                <v-row justify="center">
                  <v-btn :to="`/?example=${items[model].id}`"  @click="$router.go()" color="primary">{{$t("examples.load")}}</v-btn>
                </v-row>
              </v-col>
            </v-row>
          </v-sheet>
        </v-expand-transition>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  // the title and description for each example is in the langs folder according to the id
  data: () => ({
    model: 0,
    items: [
      {
        id: "partidos-politicos",
        src: require(`../assets/ex/partidos-politicos.png`)
      },
      {
        id: "operacao-marques",
        src: require(`../assets/ex/operacao-marques.png`)
      },
      {
        id: "presidentes-portugueses",
        src: require(`../assets/ex/presidentes-portugueses.png`)
      },
      {
        id: "dos-santos",
        src: require(`../assets/ex/dos-santos.png`)
      },
      {
        id: "estados-desunidos",
        src: require(`../assets/ex/estados-desunidos.png`)
      },
      {
        id: "gato-fedorento",
        src: require(`../assets/ex/gato-fedorento.png`)
      },
      {
        id: "sociedades-pouco-secretas",
        src: require(`../assets/ex/sociedades-pouco-secretas.png`)
      },
      {
        id: "nobel",
        src: require(`../assets/ex/nobel.png`)
      },
      {
        id: "fatima-futebol-fado",
        src: require(`../assets/ex/fatima-futebol-fado.png`)
      }
    ]
  }),
  created() {
    // this.model = Math.floor(Math.random() * this.items.length)
  }
};
</script>
