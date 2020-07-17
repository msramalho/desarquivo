<template>
  <v-snackbar v-model="snackbar" :multi-line="multiLine">
    {{ text }}
    <v-btn color="red" text>Close</v-btn>
  </v-snackbar>
</template>

<script>
export default {
  props: {
    snackbar: {
      text: ""
    },
      multiLine: true
  }
};
</script>