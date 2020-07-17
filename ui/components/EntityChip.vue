<template>
  <div>
    <v-chip
      v-for="e in entities"
      :key="e._id"
      v-on:click="addEntity({_id:e._id, label:label, text:e.text})"
      class="ml-1 mb-1"
      :color="color"
      outlined
      label
      small
    >
      <v-icon left>{{icon}}</v-icon>
      <span style="color:black">{{e.text}}</span>
    </v-chip>
  </div>
</template>

<script>
export default {
  props: {
    entities: Array,
    label: String
  },
  methods: {
    addEntity(e) {
      this.$emit("addEntity", e);
    }
  },
  computed: {
    color: function() {
      if(this.label == "PER") return "#009688"
      if(this.label == "ORG") return "#673AB7"
      if(this.label == "LOC") return "#00B8D4"
      if(this.label == "MISC") return "#263238"
    },
    icon: function() {
      if(this.label == "PER") return "mdi-account-outline"
      if(this.label == "ORG") return "mdi-office-building"
      if(this.label == "LOC") return "mdi-map-marker"
      if(this.label == "MISC") return "mdi-dots-horizontal-circle-outline"
    }
  }
};
</script>