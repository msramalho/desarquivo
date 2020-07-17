<template>
  <v-layout>
    <Canvas />
  </v-layout>
</template>

<script>
import Canvas from "~/components/Canvas.vue";

export default {
  components: { Canvas },
  mounted() {
    // used to wake up the heroku container
    this.$axios
      .get("/")
      .then(res => {
        this.$toast.info(this.$t("index.server.ready"), {
          x: "right",
          y: "bottom",
          timeout: 1000
        });
      })
      .catch(e => {
        console.log(e);
        this.$toast.warning(this.$t("index.server.inaccessible"), {
          x: "right",
          y: "bottom",
          timeout: 4000
        });
      });
  }
};
</script>
