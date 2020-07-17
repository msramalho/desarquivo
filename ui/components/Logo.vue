<template>
  <div class="holder animate">
    <v-icon color="white" class="animate-icon">mdi-graph-outline</v-icon>
    <span class="animate-text">Desarquivo</span>
    <span class="animate-text-final">esarquivo</span>
  </div>
</template>

<style scoped>
.holder {
  font-size: 20px;
}
.animate {
  margin-right: -100px;
}
.animate,
.animate-text-final,
.animate-icon {
  display: inline-block;
  transition: all 1s ease-in-out;
}
.animate .animate-text {
  opacity: 1;
  transition: opacity 0.5s;
}
.animate .animate-text-final {
  opacity: 0;
  transform: translateX(200px);
  transition: opacity 0.5s, transform 0.5s;
  margin-left: -7px;
}
.animate .animate-icon {
  transform: rotate(0deg);
  transition: transform 0.5;
}
.animate:hover {
  cursor: none;
}
.animate:hover .animate-text {
  opacity: 0;
}
.animate:hover .animate-text-final {
  opacity: 1;
  transform: translateX(-100px);
}
.animate:hover .animate-icon {
  transform: rotate(-270deg);
  transition: transform 0.5s;
}
</style>